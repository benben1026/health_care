__author__ = 'tang'


from crawl import Getter
from bs4 import BeautifulSoup

t = Getter("NHS.data")
for c in range(65, 91):
    t.traverse_alphabet_index(chr(c))
t.save()
