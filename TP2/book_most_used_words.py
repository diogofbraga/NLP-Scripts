from bs4 import BeautifulSoup
import requests
import re
import time
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
import nltk

def parseHTML(url):
    text_url = url
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')
    return  text_soup.get_text()

def getStopwords(num):
    # remover stopwords : escolher uma das opcoes consoante a flag
    if num == '100':
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF100.txt'
    elif num == '200':
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF200.txt'
    else:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF300.txt'

    stopwords_content = requests.get(stopwords_url).text
    stopwords_soup = BeautifulSoup(stopwords_content,'lxml')
    return stopwords_soup.get_text()

def lower(flag,list):
    # lower se tiver flag de ignore case
    if flag:
        return [w.lower() for w in list]
    else:
        return list

def parse_words_without_NLTK():
    start = time.time()
    print('STARTED PARSING WITHOUT NLTK')
    # dom casmurro de machado de assis
    # passar url como argumento ?
    text = parseHTML('https://www.gutenberg.org/files/55752/55752-h/55752-h.htm')

    words = re.findall(r"\w+",text,re.UNICODE)
    
    # check flag
    lower_words = lower(True, words)

    stopwords_text = getStopwords('300')

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

    end = time.time()
    print('Elapsed time: ',end - start, 'seconds')

    plt.plot()
    # close plot
    plt.clf()


def parse_words_with_NLTK():
    start = time.time()
    print('STARTED PARSING WITH NLTK')
    # dom casmurro de machado de assis
    # passar url como argumento ??
    text = parseHTML('https://www.gutenberg.org/files/55752/55752-h/55752-h.htm')

    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)

    # lower se tiver flag de ignore case
    # check flag
    words = lower(True, tokens)
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