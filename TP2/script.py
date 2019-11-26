from bs4 import BeautifulSoup
import requests
import re
import time
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
import nltk
import sys
from getopt import getopt
from urllib.parse import urlparse


def parseHTML(url):
    text_url = url
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')
    return text_soup.get_text()


def getStopwords(num):
    # remover stopwords : escolher uma das opcoes consoante a flag
    if num == 100:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF100.txt'
    elif num == 200:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF200.txt'
    else:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF300.txt'

    stopwords_content = requests.get(stopwords_url).text
    stopwords_soup = BeautifulSoup(stopwords_content, 'lxml')
    return stopwords_soup.get_text()


def lower(flag, list):
    # lower se tiver flag de ignore case
    if flag:
        return [w.lower() for w in list]
    else:
        return list


def parseWordsNoNLTK(html):
    start = time.time()
    print('STARTED PARSING WITHOUT NLTK')
    # dom casmurro de machado de assis

    text = parseHTML(html)

    words = re.findall(r"\w+", text, re.UNICODE)
    print('words: ', len(words))

    return words,start

def lowerNoNLTK(words):
    # check flag
    lower_words = lower(True, words)

    return lower_words

def stopWordsNoNLTK(lower_words,start,num,p):

    stopwords_text = getStopwords(num)

    stopwords = re.findall(r'\w+', stopwords_text, re.UNICODE)
    print('stopwords: ', len(stopwords))

    clean_words = [w for w in lower_words if w not in stopwords]
    print('clean words: ', len(clean_words))

    print('counting word frequency...')
    word_count = [clean_words.count(w) for w in clean_words]
    # transform list in dictionary
    dictionary = dict(list(zip(clean_words, word_count)))

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
    plt.bar(range(p), values[:p], tick_label=names[:p])
    plt.xticks(rotation=25, fontsize=7.5)

    end = time.time()
    print('Elapsed time: ', end - start, 'seconds')

    plt.show()
    # close plot
    plt.clf()




def parseWordsNLTK(html):
    start = time.time()
    print('STARTED PARSING WITH NLTK')
    # dom casmurro de machado de assis

    text = parseHTML(html)

    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)

    return tokens,start

def lowerNLTK(tokens):
    # lower se tiver flag de ignore case
    # check flag
    words = lower(True, tokens)
    print('words: ', len(words))

    return words

def getStopwordsNLTK(words,start):
    # usar stopwords se tiver flag
    stopwords = nltk.corpus.stopwords.words('portuguese')
    print('stopwords: ', len(stopwords))
    clean_words = [word for word in words if word not in stopwords]
    print('clean words: ', len(clean_words))

    freqdist = nltk.FreqDist(clean_words)

    end = time.time()
    print('Elapsed time: ', end - start, 'seconds')

    return freqdist

def plot_NLTK(freqdist,num):
    # em vez de 10, pôr X consoante a flag
    freqdist.plot(num)
    # close plot
    plt.clf()


def main():
    opts, args = getopt(sys.argv[1:], "mnlsu:N:p:")
    dop = dict(opts)

    #html = 'https://www.gutenberg.org/files/55752/55752-h/55752-h.htm';

    if "-u" in dop:
        html = dop.get('-u')

    if "-m" in dop:
        words,start = parseWordsNoNLTK(html)
        if "-l" in dop:
            words = lowerNoNLTK(words)
        if "-N" in dop:
            numSW = int(dop.get('-N',100))
        else: numSW = 100
        if "-p" in dop:
            numP = int(dop.get("-p"))
        else: numP = 10
        stopWordsNoNLTK(words,start,numSW,numP)

    if "-n" in dop:
        words,start = parseWordsNLTK(html)
        if "-l" in dop:
            words = lowerNLTK(words)
        if "-s" in dop:
            freqdist = getStopwordsNLTK(words,start)
        else:
            freqdist = nltk.FreqDist(words)
        if "-p" in dop:
            numP = int(dop.get('-p'))
        else: numP = 10
        plot_NLTK(freqdist,numP)

main()
