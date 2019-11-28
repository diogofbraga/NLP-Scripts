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

    if flag:
        return [w.lower() for w in list]
    else:
        return list


def parseWordsNoNLTK(html):
    start = time.time()
    print('STARTED PARSING WITHOUT NLTK')

    text = parseHTML(html)

    words = re.findall(r"\w+", text, re.UNICODE)
    print('words: ', len(words))

    return words,start

def lowerNoNLTK(words):

    lower_words = lower(True, words)

    return lower_words

def stopWordsNoNLTK(lower_words,num):

    stopwords_text = getStopwords(num)

    stopwords = re.findall(r'\w+', stopwords_text, re.UNICODE)
    print('stopwords: ', len(stopwords))

    clean_words = [w for w in lower_words if w not in stopwords]
    print('clean words: ', len(clean_words))

    return clean_words

def plotNoNLTK(clean_words,start,p):

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

    # default 10
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

    text = parseHTML(html)

    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)

    return tokens,start

def lowerNLTK(tokens):
    # check flag
    words = lower(True, tokens)
    print('words: ', len(words))

    return words

def getStopwordsNLTK(words):

    stopwords = nltk.corpus.stopwords.words('portuguese')
    print('stopwords: ', len(stopwords))
    clean_words = [word for word in words if word not in stopwords]
    print('clean words: ', len(clean_words))

    freqdist = nltk.FreqDist(clean_words)

    return freqdist

def plotNLTK(freqdist,num,start):
    end = time.time()
    print('Elapsed time: ', end - start, 'seconds')

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
            numSW = int(dop.get('-N'))
        else: numSW = 100
        if "-s" in dop:
            words = stopWordsNoNLTK(words,numSW)
        if "-p" in dop:
            numP = int(dop.get("-p"))
        else: numP = 10
        plotNoNLTK(words,start,numP)

    elif "-n" in dop:
        words,start = parseWordsNLTK(html)
        if "-l" in dop:
            words = lowerNLTK(words)
        if "-s" in dop:
            freqdist = getStopwordsNLTK(words)
        else:
            freqdist = nltk.FreqDist(words)
        if "-p" in dop:
            numP = int(dop.get('-p'))
        else: numP = 10
        plotNLTK(freqdist,numP,start)

main()
