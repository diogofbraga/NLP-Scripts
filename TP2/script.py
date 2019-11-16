#!/usr/bin/env python

# Store url
url = 'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm'

import requests

# Make the request and check object type
r = requests.get(url)
type(r)

# Extract HTML from Response object and print
html = r.text
#print(html)

# Import BeautifulSoup from bs4
from bs4 import BeautifulSoup


# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "lxml") # or "html.parser"
type(soup)

# Get soup title
soup.title
print(soup.title)

# Get soup title as string
soup.title.string

# Get hyperlinks from soup and check out first several
soup.findAll('a')[:8]

# Get the text out of the soup and print it
text = soup.get_text()
#print(text)
