__author__ = 'tang'


from position import PosGetter
from bs4 import BeautifulSoup

t = PosGetter("NHS.data", read=True)
t.to_database_format(open("NHS_DB.data", "w"))


# t.to_database_format(open("NHS_DB.data", "w"))
