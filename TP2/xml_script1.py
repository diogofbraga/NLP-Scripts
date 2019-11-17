# -*- coding: utf-8 -*-
#!/usr/bin/env python

from bs4 import BeautifulSoup
import re
import unicodedata

path = "test1.xml"
infile = open(path,"r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')
pages = soup.findAll('page')

pattern = "Proverbios"
proverbios = []

for page in pages:
    title = page.find('title')
    title = unicodedata.normalize('NFKD', title.get_text()).encode('ASCII', 'ignore')

    if (re.search(pattern, title)):
        #print(title.get_text())
        text = page.find('text')
        #print(text.get_text())
        proverbios = re.findall(r"Com céu azul carregado",text.get_text())

print(proverbios)
