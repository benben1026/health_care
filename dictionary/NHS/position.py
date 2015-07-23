__author__ = 'Tang'
from BaseGetter import BaseGetter
import urllib2
from bs4 import BeautifulSoup

class PosGetter(BaseGetter):
    level1 = ["Head", "Chest", "Arm", "Abdomen", "Leg"]

    def __init__(self, path, read):
        BaseGetter.__init__(self, path, read)
        self.diseases_link_index = {}
        self.create_index()

    def create_index(self):
        for c in range(65, 91):
            alphabet = chr(c)
            for term in self.content[alphabet]["index"]:
                term_obj = self.content[alphabet]["index"][term]
                self.diseases_link_index[term_obj["link"]] = term_obj
                for sub_term in term_obj["sub_layer"]:
                    self.diseases_link_index[term_obj["sub_layer"][sub_term]["link"]] = term_obj["sub_layer"][sub_term]

    def traverse(self):
        self.traverse_level1("Male")
        self.traverse_level1("Female")

    def traverse_level1(self, gender):
        for level1_pos in self.level1:
            self.traverse_level2(gender, level1_pos)

    def traverse_level2(self, gender, level1_pos):
        url = "http://www.nhs.uk/Conditions/Pages/bodymap.aspx?LevelOne={0}&Gender={1}".format(level1_pos, gender)
        try:
            level2_page = urllib2.urlopen(url)
        except urllib2.URLError:
            self.url_error_handler(url)
            return False
        level2_pos_container = BeautifulSoup(level2_page, "html.parser").find(id="haz-mod3").find("ul", recursive=False)
        for level2_pos in level2_pos_container.find_all("li", recursive=False):
            diseases_link = level2_pos.find("a")["href"]
            level2 = level2_pos.text
            # Escape
            diseases_link = diseases_link.replace(" ", "%20")
            try:
                diseases_page = urllib2.urlopen("http://www.nhs.uk/Conditions/Pages/bodymap.aspx" + diseases_link)
            except urllib2.URLError:
                self.url_error_handler(diseases_link)
                return
            diseases_container = BeautifulSoup(diseases_page, "html.parser").find(id="haz-mod4").find("ul")
            for disease_item in diseases_container.find_all("li", recursive=False):
                disease_element = disease_item.find("a")
                disease_name = disease_element.text
                disease_link = disease_element["href"]
                self.pos_match(gender, level1_pos, level2, disease_name, disease_link)

    def pos_match(self, gender, level1, level2, disease_name, disease_link):
        print("matched")
        if disease_link in self.diseases_link_index:
            disease_obj = self.diseases_link_index[disease_link]
            if "data" not in disease_obj:
                return
            if "gender" not in disease_obj["data"]:
                disease_obj["data"]["gender"] = {gender: True}
            else:
                disease_obj["data"]["gender"][gender] = True
            if "position" not in disease_obj["data"]:
                disease_obj["data"]["position"] = {}
            disease_obj["data"]["position"] = {"level1": level1, "level2": level2}
