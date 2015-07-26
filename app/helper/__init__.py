__author__ = 'Tang'


def retrieve_subtitle(s):
    rv = {}
    paragraph_list = s.split("#%#")
    index = 1
    while index < len(paragraph_list):
        rv[paragraph_list[index]] = paragraph_list[index + 1]
        index += 2
    return rv
