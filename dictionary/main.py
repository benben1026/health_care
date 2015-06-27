__author__ = 'Tang'

import urllib2
from bs4 import BeautifulSoup
import json

recorded_field = ["Causes", "Exams and Tests", "Treatment", "Possible Complications", "Prevention"]

def traverse(node):
    if not node.name:
        return node.string
    if node.name == "ul":
        items = []
        for item in node.children:
            items.append(traverse(item))

        return ', '.join(items) + ". "
    else:
        con = ""
        for child in node.children:
            con += traverse(child)
        return con


def find_lis(node):
    rv = []
    lis = node.find_all('li')
    for li in lis:
        rv.append(traverse(li))
    return rv

def med_plus(page_name, page_content):
    disease = {}
    soup = BeautifulSoup(page_content)
    article = soup.find("div", {"id": "d-article"})
    main_content = article.find("div", {"class": "main"})
    if not main_content:
        main_content = article.find("div", {"class": "main-single"})
    title = soup.find("h1").string
    if title != page_name:
        print("Ambiguous name {0} and {1}".format(title, page_name))
    sections = main_content.children
    for section in sections:
        if section.name == "section":
            section_name = section.find("div", {"class": "section-title"}).contents[0].string
            section_body = section.find("div", {"class": "section-body"})
            if section_name == "Symptoms":
                symptoms = find_lis(section_body)
                disease[section_name] = symptoms
            else:
                if section_name in recorded_field:
                    section_body_content = traverse(section_body)
                    disease[section_name] = section_body_content
        elif section.name == "p":
            disease["description"] = section.text
    return disease

def parse_raw(raw, output):
    rv = {}
    fp = open(raw)
    data = json.load(fp)
    fp.close()
    for disease_name in data:
        rv[disease_name] = med_plus(disease_name, data[disease_name])
    fp_out = open(output, "w")
    json.dump(rv, fp_out)

def filter_disease(med_file, output):
    fp = open(med_file)
    med_data = json.load(fp)
    fp.close()
    rv = {}
    for item_name in med_data:
        if "Symptoms" in med_data[item_name] and med_data[item_name]["Symptoms"]:
            rv[item_name] = med_data[item_name]
    fp = open(output, "w")
    json.dump(rv, fp)
    fp.close()


def parse_symptom(disease_file, dict_path, output):
    pass


def get_all_med_plus():
    for index in range(65, 91):
        c = chr(index)
        url = "http://www.nlm.nih.gov/medlineplus/ency/encyclopedia_{0}.htm".format(c)
        index_page = BeautifulSoup(urllib2.urlopen(url))
        index_container = index_page.find("ul", {"id": "index"})
        rv = {}
        for item_tag in index_container.find_all("a", href=True):
            item_name = item_tag.text
            print(item_name.encode("utf-8"))
            item_url = "http://www.nlm.nih.gov/medlineplus/ency/{0}".format(item_tag["href"])
            try:
                content_fp = urllib2.urlopen(item_url)
                rv[item_name] = content_fp.read()
            except:
                print(item_url + " || failed")

        f = open("D:/raw_data_" + chr(index), 'w')
        json.dump(rv, f)
        f.close()
        print "====================={0} Complete=======================".format(chr(index))
