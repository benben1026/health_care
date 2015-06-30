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
        elif isinstance(s, dict):
            obj = s
        return Symptom(obj['keys'], obj['name'], obj['pos'])

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
            lower_key = key.lower()
            lower_desc = desc.lower()
            lower_pos = None
            if self.pos:
                lower_pos = self.pos.lower()
            if lower_key in lower_desc and (not lower_pos or lower_pos in lower_desc):
                key_match = True

        return key_match
