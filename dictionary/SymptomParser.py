__author__ = 'Tang'

import json
from Symptom import Symptom

class SymptomParser:
    def __init__(self, dictionary):
        self.dict_path = dictionary
        if not self.load_dict():
            self.dictionary = []
            self.index = {}

    def load_dict(self):
        dict_file = None
        try:
            dict_file = open(self.dict_path)
            dict_json = json.load(dict_file)
        except:
            return False
        for symptom_name in dict_json:
            if symptom_name in self.index:
                raise ItemError("Duplicate symptom name: " + symptom_name)
            symptom = Symptom.restore(dict_json[symptom_name])
            self.dictionary.append(symptom)
            self.index[symptom_name] = symptom
        dict_file.close()
        return True

    def save_dict(self):
        try:
            dict_file = open(self.dict_path, "w")
            json.dump(self.dictionary, dict_file)
        except:
            print("SymptomParser: Save Failed")

    def parse(self, desc):
        rv = []
        for symptom in self.dictionary:
            if symptom.match(desc):
                rv.append(symptom)
        return rv

    def add_symptom(self, symptom):
        self.dictionary.append(symptom)
        self.index[symptom.name] = symptom

    def input_parse(self, i, desc):
        items = i.split('|')
        items = self.strip_all(items)
        rv = []
        for item in items:
            parts = item.split('>')
            if len(parts) == 2:
                key = parts[0]
                name = parts[1]
            else:
                key = name = parts[0]
            if key not in desc:
                raise ItemError("Can not find key in symptom description")
            if name in self.index:
                symptom = self.index[name]
                symptom.add_key(key)
                rv.append(symptom)
            else:
                new_symptom = Symptom(key, name)
                self.add_symptom(new_symptom)
                rv.append(new_symptom)

        return rv

    @staticmethod
    def strip_all(str_list):
        rv = []
        for s in str_list:
            rv.append(s.strip())
        return rv

class ItemError(Exception):
    def __init__(self, message):
        super(ItemError, self).__init__(message)