__author__ = 'Tang'

import json

class BaseGetter:
    def __init__(self, path, read=False):
        self.progress = None
        self.content = None
        self.error = None
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
            try:
                self.content = data["content"]
            except KeyError:
                self.content = {}
            try:
                self.progress = data["progress"]
            except KeyError:
                self.progress = {}
            try:
                self.error = data["error"]
            except KeyError:
                self.error = []
        else:
            self.content = {}
            self.progress = {}
            self.error = []

    def save(self):
        json.dump({"content": self.content, "progress": self.progress, "error": self.error}, self.f)

    def url_error_handler(self, link):
        print("Can not open link {0}".format(link))
        self.error.append(["URL error", link])

    def strip(self):
        self.strip_obj(self.content)

    @classmethod
    def strip_list(cls, obj):
        for key in range(0, len(obj)):
            if isinstance(obj[key], dict):
                cls.strip_obj(obj[key])
            if isinstance(obj[key], list):
                cls.strip_list(obj[key])
            if isinstance(obj[key], str) or isinstance(obj[key], unicode):
                obj[key] = obj[key].strip()

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
    def strip_obj(cls, obj):
        for key in obj:
            if isinstance(obj[key], dict):
                cls.strip_obj(obj[key])
            if isinstance(obj[key], list):
                cls.strip_list(obj[key])
            if isinstance(obj[key], str) or isinstance(obj[key], unicode):
                obj[key] = obj[key].strip()

