__author__ = 'Tang'

import json
from Symptom import Symptom


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Symptom):
            return o.__dict__


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
        self.dictionary = []
        self.index = {}
        for symptom in dict_json:
            if symptom["name"] in self.index:
                raise ItemError("Duplicate symptom name: " + symptom["name"])
            symptom_obj = Symptom.restore(symptom)
            self.add_symptom(symptom_obj)
        dict_file.close()
        return True

    def save_dict(self):
        try:
            dict_file = open(self.dict_path, "w")
            dict_str = CustomEncoder().encode(self.dictionary)
            dict_file.write(dict_str)
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
        if symptom.name in self.index:
            self.index[symptom.name].append(symptom)
        else:
            self.index[symptom.name] = [symptom]

    def has_symptom(self, name, pos):
        for symptom in self.index[name]:
            if symptom.pos == pos:
                return True
        return False

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
            pos_split = name.split('@')
            if len(pos_split) == 2:
                name = pos_split[0]
                pos = pos_split[1]
            else:
                pos = None
            if pos:
                if pos.lower() not in desc.lower():
                    self.save_dict()
                    raise ItemError("Can not find position in symptom description")
            if key.lower() not in desc.lower():
                self.save_dict()
                raise ItemError("Can not find key in symptom description")
            if name.lower() in self.index:
                symptom = self.index[name]
                symptom.add_key(key)
                rv.append(symptom)
            else:
                new_symptom = Symptom(key, name, pos)
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