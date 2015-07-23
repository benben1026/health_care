__author__ = 'zhou'

from pubmed import PubmedGetter
from bs4 import BeautifulSoup

t = PubmedGetter("Anal fistula")
t.send()

print(t.extract())