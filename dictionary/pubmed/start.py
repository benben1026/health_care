__author__ = 'zhou'

from pubmed import PubmebGetter
from bs4 import BeautifulSoup

t = PubmebGetter("Anal fistula")
t.send()

print(t.extract())