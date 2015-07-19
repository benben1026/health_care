__author__ = 'tang'

import tempfile, urllib2, json
from bs4 import BeautifulSoup


class Getter:
    def __init__(self, path):
        self.progress = None
        self.content = None
        self.f = None
        if not path:
            path = "NHS.data"
        self.load(path)

    def create(self, path):
        self.f = open(path, "w")

    def load(self, path):
        data = None
        try:
            self.f = open(path, "r")
            try:
                data = json.load(self.f)
            except ValueError:
                pass
            self.f.close()
            self.f = open(path, "w")
        except IOError:
            print("Can not open file {0}".format(path))
            self.create(path)
        if data:
            self.content = data["content"]
            self.progress = data["content"]
        else:
            self.content = {}
            self.progress = {}

    def save(self):
        json.dump({"content": self.content, "progress": self.progress}, self.f)

    def traverse_alphabet_index(self, alphabet):
        if alphabet in self.progress:
            return True

        index_url = "http://www.nhs.uk/Conditions/Pages/BodyMap.aspx?Index={}".format(alphabet)
        try:
            index_page = urllib2.urlopen(index_url)
        except urllib2.URLError:
            print("Can not open index page {0}".format(index_url))
            return False
        rv = {}
        soup = BeautifulSoup(index_page, 'html.parser')
        container = soup.find(id="ctl00_PlaceHolderMain_BodyMap_ConditionsByAlphabet")

        # Handle Continue
        last_first_info = None
        for sub_category in container.find_all("div", {"class": "index-section"}):
            for first_layer_container in sub_category.find_all("ul", recursive=False):
                for first_layer_item in first_layer_container.find_all("li", recursive=False):
                    first_info = first_layer_item.find('a', recursive=False)
                    if not first_info:
                        # Can not find title information
                        if first_layer_item["class"][0] == "continued":
                            # Handle continue
                            first_info = last_first_info
                        else:
                            print("Can not process paragraph {0}".format(first_layer_item.text))
                    else:
                        # A new first layer category
                        last_first_info = first_info
                        rv[first_info.text] = {"link": first_info["href"], "sub_layer": {}}
                    this_layer = rv[first_info.text]
                    second_layer_container = first_layer_item.find("ul", recursive=False)
                    if second_layer_container:
                        for second_layer_item in second_layer_container.find_all("li", recursive=False):
                            second_info = second_layer_item.find("a")
                            this_layer["sub_layer"][second_info.text] = {"link": second_info["href"]}

        if alphabet not in self.progress:
            self.progress[alphabet] = {}
        self.progress[alphabet]["index"] = True
        if alphabet not in self.content:
            self.content[alphabet] = {}
        self.content[alphabet]["index"] = rv
        print("Index of alphabet {0} complete".format(alphabet))
        return True

    def crawl_page(self, url, alphabet):
        pass

    @staticmethod
    def is_disease(soup):
        # Check whether there is an symptoms link in nav-bar
        container = soup.find(id="ctl00_PlaceHolderMain_articles")
        for link in container.find_all("a"):
            if "Symptoms" in link.text:
                return True
        # Check whether there is an symptoms description in introduction
        container = soup.find(class_="main-content")
        for title in container.find_all('h3'):
            if "symptoms" in title.text.lower() or "symptom" in title.text.lower():
                return True

        return False
