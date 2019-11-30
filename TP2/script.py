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
    # Fazer pedido GET para obter o objecto HTML em formato texto
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')
    # Obter apenas o texto da pagina HTML, sem as tags deste
    return text_soup.get_text()

def getStopwords(num):
    if num == 100:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF100.txt'
    elif num == 200:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF200.txt'
    else:
        stopwords_url = 'https://www.linguateca.pt/chave/stopwords/publico.MF300.txt'

    # fazer pedido GET para obter o texto do HTML com as stopwords
    stopwords_content = requests.get(stopwords_url).text
    # Criar objeto BS, usando o lxml
    stopwords_soup = BeautifulSoup(stopwords_content, 'lxml')
    # Obter a lista de stopwords, extraindo-as da div
    return stopwords_soup.get_text()

def lower(flag, list):
    # se a flag de lower estiver ativada,
    # transformar todas as letras das palavras em minusculas
    # caso contrario, devolve a lista que recebeu como parametro
    if flag:
        return [w.lower() for w in list]
    else:
        return list

def lower_res(tokens):
    words = lower(True, tokens)
    print('words: ', len(words))

    return words

def parseWordsNoNLTK(html):
    # iniciar contador de tempo
    start = time.time()
    print('STARTED PARSING WITHOUT NLTK')

    text = parseHTML(html)

    # obter todas as palavras presentes no texto
    # obtido do parseHTML, com a Regex \w+, no formato UNICODE
    words = re.findall(r"\w+", text, re.UNICODE)
    print('words: ', len(words))

    return words,start

def stopWordsNoNLTK(lower_words,num):
    stopwords_text = getStopwords(num)

    # extrai todas as palavras (\w+) do texto com as stopwords
    stopwords = re.findall(r'\w+', stopwords_text, re.UNICODE)
    print('stopwords: ', len(stopwords))

    # remove da lista de palavras aquelas que se encontram
    # na lista de stopwords
    clean_words = [w for w in lower_words if w not in stopwords]
    print('clean words: ', len(clean_words))

    return clean_words

def plotNoNLTK(clean_words,start,p):
    print('counting word frequency...')
    # conta as ocorrencias das palavras e coloca-as numa lista
    word_count = [clean_words.count(w) for w in clean_words]
    # transforma lista de ocorrencias e de palavras num dicionario
    dictionary = dict(list(zip(clean_words, word_count)))

    print('sorting by frequency...')
    # transforma o dicionário numa lista de pares e ordena-os por
    # numero de ocorrencias, revertendo no final a ordem para ordem
    # decrescente
    sorted_list = [(dictionary[key], key) for key in dictionary]
    sorted_list.sort()
    sorted_list.reverse()

    # obtem a informacao dos pares e coloca-a na respetiva lista
    # separando as palavras e as respetiva ocorrencias
    names = [val[1] for val in sorted_list]
    values = [val[0] for val in sorted_list]

    # desenhar o grafico com P barras, utilizando o matplotlib
    print('Drawing graph...')
    plt.bar(range(p), values[:p], tick_label=names[:p])
    plt.xticks(rotation=25, fontsize=7.5)

    # contabiliza o tempo que demorou a efetuar o processamento
    end = time.time()
    print('Elapsed time: ', end - start, 'seconds')

    # mostra o grafico
    plt.show()
    # close plot
    plt.clf()


def parseWordsNLTK(html):
    # inicialização do temporizador
    start = time.time()
    print('STARTED PARSING WITH NLTK')

    text = parseHTML(html)

    # utilizando o tokenizer do NLTK, obtem a lista de
    # palavras existentes na obra
    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)

    return tokens,start

def getStopwordsNLTK(words):
    # obter as stopwords da corpora do nltk
    stopwords = nltk.corpus.stopwords.words('portuguese')
    print('stopwords: ', len(stopwords))
    # remover da lista de palavras aquelas que se encontram na lista
    # de stopwords
    clean_words = [word for word in words if word not in stopwords]
    print('clean words: ', len(clean_words))

    # obter o grafico de frequências das palavras da lista
    freqdist = nltk.FreqDist(clean_words)

    return freqdist

def plotNLTK(freqdist,num,start):
    # finalizacao do temporizador, imprimindo o tempo de execucao
    end = time.time()
    print('Elapsed time: ', end - start, 'seconds')

    # desenhar o gráfico
    freqdist.plot(num)
    # close plot
    plt.clf()


def main():
    # obter argumentos do script
    opts, args = getopt(sys.argv[1:], "mnlsu:N:p:")
    # colocar argumentos num dicionário
    dop = dict(opts)

    #html = 'https://www.gutenberg.org/files/55752/55752-h/55752-h.htm';

    # flag para o url da obra a processar
    if "-u" in dop:
        html = dop.get('-u')

    # para versão sem NLTK
    if "-m" in dop:
        words,start = parseWordsNoNLTK(html)
        # flag lower / ignore case
        if "-l" in dop:
            words = lower_res(words)
        # numero de stopwords a utilizar (100, 200 ou 300)
        if "-N" in dop:
            numSW = int(dop.get('-N'))
        # por default, usa 100
        else: numSW = 100
        # flag de stopwords
        if "-s" in dop:
            words = stopWordsNoNLTK(words,numSW)
        # flag p - número de barras a mostrar no gráfico
        # por default, são 10
        if "-p" in dop:
            numP = int(dop.get("-p"))
        else: numP = 10
        plotNoNLTK(words,start,numP)

    # para versão com NLTK
    elif "-n" in dop:
        words,start = parseWordsNLTK(html)
        # flag lower / ignore case
        if "-l" in dop:
            words = lower_res(words)
        # flag de stopwords
        if "-s" in dop:
            freqdist = getStopwordsNLTK(words)
        else:
            freqdist = nltk.FreqDist(words)
        # flag p - número de barras a mostrar no gráfico
        # por default, são 10
        if "-p" in dop:
            numP = int(dop.get('-p'))
        else: numP = 10
        plotNLTK(freqdist,numP,start)

# correr o script
main()
