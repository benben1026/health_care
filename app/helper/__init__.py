__author__ = 'Tang'


def retrieve_subtitle(s):
    rv = {}
    paragraph_list = s.split("#%#")
    index = 1
    while index < len(paragraph_list):
        rv[paragraph_list[index]] = paragraph_list[index + 1]
        index += 2
    return rv

def password_hash(s):
    import hashlib
    hash_obj = hashlib.sha256()
    hash_obj.update(s)
    return hash_obj.hexdigest()

