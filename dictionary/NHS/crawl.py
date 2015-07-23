__author__ = 'tang'

import tempfile, urllib2, json
from bs4 import BeautifulSoup, NavigableString


class Getter:
    def __init__(self, path, read=False):
        self.progress = None
        self.content = None
        self.f = None
        if not path:
            path = "NHS.data"
        self.load(path, read=read)

    def create(self, path):
        self.f = open(path, "w")

    def load(self, path, read=False):
        data = None
        try:
            self.f = open(path, "r")
            try:
                data = json.load(self.f)
            except ValueError:
                pass
            self.f.close()
            if read:
                self.f = open(path, "r")
            else:
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

    def traverse_alphabet(self, alphabet):
        if alphabet not in self.progress:
            self.progress[alphabet] = {}
        if "content" in self.progress[alphabet] and self.progress[alphabet]["content"]:
            return 0, 0
        count = 0
        satisfied = 0
        container = self.content[alphabet]["index"]
        for item in container:
            count += 1
            if self.test_page(item, container[item]):
                satisfied += 1
            for sub_item in container[item]["sub_layer"]:
                count += 1
                if self.test_page(sub_item, container[item]["sub_layer"][sub_item]):
                    satisfied += 1
        self.progress[alphabet]["content"] = True

        return count, satisfied

    def to_database_format(self, fp=None):
        index = {}
        rv = {}
        for c in range(65, 91):
            alphabet = chr(c)
            for name in self.content[alphabet]["index"]:
                item = self.content[alphabet]["index"][name]
                link = item["link"]
                if link not in index:
                    index[link] = True
                    if "data" in item:
                        rv[name] = item["data"]
                for sub_name in item["sub_layer"]:
                    sub_item = item["sub_layer"][sub_name]
                    sub_link = sub_item["link"]
                    if sub_link not in index:
                        index[sub_link] = True
                        if "data" in sub_item:
                            rv[sub_name] = sub_item["data"]

        if fp:
            json.dump(rv, fp)
        return rv

    @classmethod
    def test_page(cls, name, container):
        try:
            cls.craw_page(name, container)
        except:
            return False
        return True

    @classmethod
    def craw_page(cls, name, container):
        print("Process page {0}".format(name))
        container["data"] = {}
        obj = container["data"]
        page = None
        try:
            if container["link"][0] == '/':
                link = "http://www.nhs.uk" + container["link"]
            else:
                return "None symptom page"
            page = urllib2.urlopen(link)
        except urllib2.URLError:
            print("Can not open term {0} with page link {1}".format(name, container["link"]))
        soup = BeautifulSoup(page)
        is_disease = cls.is_disease(soup)
        symptoms_link = None
        if is_disease:
            # If is_disease returns a link, then the symptoms are in another page
            if isinstance(is_disease, str) or isinstance(is_disease, unicode):
                symptoms_link = is_disease
                symptoms_page = None
                if symptoms_link[0] == '/':
                    symptoms_full_link = "http://www.nhs.uk" + symptoms_link
                else:
                    symptoms_full_link = symptoms_link
                try:
                    symptoms_page = urllib2.urlopen(symptoms_full_link)
                except urllib2.URLError:
                    print("Can not open symptom page of term {0}".format(name))
                if symptoms_page:
                    symptoms_soup = BeautifulSoup(symptoms_page)
                    symptoms_list = cls.parse_symptom(symptoms_soup)
                    obj["Symptoms"] = symptoms_list

        # Parse introduction page
        data = cls.parse_block(soup)
        obj["Introduction"] = data
        # Traverse other blocks except symptoms block
        blocks_container = soup.find(id="ctl00_PlaceHolderMain_articles")
        for link in blocks_container.find_all("a"):
            if link["href"] and link["href"] != symptoms_link:
                link_text = [text for text in link.stripped_strings]
                cls.craw_block(obj, link_text[1], link["href"])

        return container

    @classmethod
    def craw_block(cls, obj, block_name, link):
        block_page = None
        if link[0] == '/':
            link = "http://www.nhs.uk" + link
        try:
            block_page = urllib2.urlopen(link)
        except urllib2.URLError:
            print("Can not open block {0}".format(block_name))

        if not block_page:
            return
        soup = BeautifulSoup(block_page)
        data = cls.parse_block(soup)
        obj[block_name] = data

    @staticmethod
    def parse_symptom(symptoms_soup):
        rv = []
        container = symptoms_soup.find(class_="main-content")
        for symptom in container.find_all("li"):
            rv.append(symptom.text)
        return rv

    @staticmethod
    def parse_block(soup):
        rv = {"Description": None}
        container = soup.find(class_="main-content")
        content_begin = False
        current_section = "Description"
        for element in container.children:
            if isinstance(element, NavigableString):
                continue
            if content_begin:
                if element.name == "h3":
                    current_section = element.text
                    rv[current_section] = None
                elif element.name != "div":
                    if rv[current_section] is None:
                        rv[current_section] = element.text
                    else:
                        rv[current_section] = rv[current_section] + " " + element.text
                    if element.name == "h4":
                        rv[current_section] += " | "

            if "Introduction" in element.text or element.name == "h2":
                content_begin = True

        return rv

    @staticmethod
    def is_disease(soup):
        # Check whether there is an symptoms link in nav-bar
        container = soup.find(id="ctl00_PlaceHolderMain_articles")
        for link in container.find_all("a"):
            if "Symptoms" in link.text:
                return link["href"]
        # Check whether there is an symptoms description in introduction
        container = soup.find(class_="main-content")
        for title in container.find_all('h3'):
            if "symptoms" in title.text.lower() or "symptom" in title.text.lower():
                return True

        return False
