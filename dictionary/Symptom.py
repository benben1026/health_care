__author__ = 'Tang'
import json

class Symptom:
    @staticmethod
    def restore(s):
        obj = None
        if isinstance(s, str):
            try:
                obj = json.loads(s)
            except ValueError:
                return None
        elif isinstance(s, list):
            obj = s
        return Symptom(obj.key, obj.name, obj.pos)

    def __init__(self, key, name=None, pos=None):
        if type(key) is list:
            self.keys = key
        else:
            if key:
                self.keys = [key]
            else:
                raise ValueError("Key can not be None")
        self.name = name
        self.pos = pos

    def add_key(self, key):
        self.keys.append(key)

    def to_json(self):
        return json.dumps(self.__dict__)

    def match(self, desc):
        key_match = False
        for key in self.keys:
            if key in desc and (not self.pos or self.pos in desc):
                key_match = True

        return key_match
