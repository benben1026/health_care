__author__ = 'tang'


from crawl import Getter

t = Getter("NHS.data")
t.traverse_alphabet('A')
t.save()