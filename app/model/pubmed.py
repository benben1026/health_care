__author__ = 'zhou'

import tempfile, urllib2, json
from bs4 import BeautifulSoup

class PubmedGetter:
	def __init__(self, keyword):
		self.keyword = keyword.replace(" ", "+")
		self.url = "http://www.ncbi.nlm.nih.gov/pubmed/?term=" + self.keyword
		self.synonym = None
		self.textarea = None

	def send(self):
		try:
			page = urllib2.urlopen(self.url)
		except urllib2.URLError:
			print("Cannot open page with keyword:" + self.keyword)
			return False
		soup = BeautifulSoup(page, 'html.parser')
		self.textarea = str(soup.find_all("textarea", class_="searchdetails_term")[0])

	def extract(self):
		#text = self.textarea[0][self.textarea[0].index('>') + 1 : self.textarea[0].index('<') - 1]
		#self.textarea = str(self.textarea[0])
		text = self.textarea[self.textarea.index('>') + 1 : self.textarea.index('<') - 1]
		text = text[0 : text.index('[MeSH Terms]')]
		text = text[1 : text.index('"', 1)]

		return text