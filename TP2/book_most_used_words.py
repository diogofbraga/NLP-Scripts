from bs4 import BeautifulSoup
import requests
import re
import time
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
import nltk

def parse_words_without_NLTK():
    start = time.time()
    print('STARTED PARSING WITHOUT NLTK')
    # dom casmurro de machado de assis
    # passar url como argumento ?
    text_url= 'https://www.gutenberg.org/files/55752/55752-h/55752-h.htm'
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')

    text = text_soup.get_text()

    words = re.findall(r"\w+",text,re.UNICODE)
    
    # lower se tiver flag de ignore case
    lower_words = [w.lower() for w in words]
    print('words: ',len(lower_words))

    # remover stopwords : escolher uma das opcoes consoante a flag
    # lista de stopwords:
    # 100 palavras: https://www.linguateca.pt/chave/stopwords/publico.MF100.txt
    # 200 palavras: https://www.linguateca.pt/chave/stopwords/publico.MF200.txt
    # 300 palavras: https://www.linguateca.pt/chave/stopwords/publico.MF300.txt
    stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF300.txt'
    stopwords_content = requests.get(stopwords_url).text
    stopwords_soup = BeautifulSoup(stopwords_content,'lxml')
    stopwords_text = stopwords_soup.get_text()

    stopwords = re.findall(r'\w+',stopwords_text,re.UNICODE)
    print('stopwords: ',len(stopwords))

    clean_words = [w for w in lower_words if w not in stopwords]
    print('clean words: ',len(clean_words))

    print('counting word frequency...')
    word_count = [clean_words.count(w) for w in clean_words]
    # transform list in dictionary
    dictionary = dict(list(zip(clean_words,word_count)))

    print('sorting by frequency...')
    # sort dictionary into list and reverse the order to be from the most used to the less
    sorted_list = [(dictionary[key], key) for key in dictionary]
    sorted_list.sort()
    sorted_list.reverse()

    # get the info from the sorted list tuples
    names = [val[1] for val in sorted_list]
    values = [val[0] for val in sorted_list]

    # default 10 : escolher numero consoante a flag
    print('Drawing graph...')
    plt.bar(range(10),values[:10],tick_label=names[:10])
    plt.xticks(rotation=25,fontsize=7.5)
    plt.plot()
    # close plot
    plt.clf()

    end = time.time()
    print('Elapsed time: ',end - start, 'seconds')

def parse_words_with_NLTK():
    start = time.time()
    print('STARTED PARSING WITH NLTK')
    # dom casmurro de machado de assis
    # passar url como argumento ??
    text_url= 'https://www.gutenberg.org/files/55752/55752-h/55752-h.htm'
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')

    text = text_soup.get_text()

    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)

    # lower se tiver flag de ignore case
    words = [token.lower() for token in tokens]
    print('words: ',len(words))
    # usar stopwords se tiver flag
    stopwords = nltk.corpus.stopwords.words('portuguese')
    print('stopwords: ',len(stopwords))
    clean_words = [word for word in words if word not in stopwords]
    print('clean words: ',len(clean_words))

    freqdist = nltk.FreqDist(clean_words)

    end = time.time()
    print('Elapsed time: ',end - start, 'seconds')

    # em vez de 10, pôr X consoante a flag
    freqdist.plot(10)
    # close plot
    plt.clf()
    

# correr uma delas consoante a flag
parse_words_without_NLTK()
# parse_words_with_NLTK()