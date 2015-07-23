__author__ = 'tang'


from crawl import Getter
from bs4 import BeautifulSoup

t = Getter("NHS.data", read=True)


t.to_database_format(open("NHS_DB.data", "w"))
