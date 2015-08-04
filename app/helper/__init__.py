__author__ = 'Tang'
from MailSender import MailSender
import jwt

jwt_secret = "NNKCWCLFM"

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


def jwt_signature(s):
    return jwt.encode(s, jwt_secret, algorithm="HS256")


def jwt_decode(s):
    try:
        return jwt.decode(s, jwt_secret, algorithms="HS256")
    except jwt.DecodeError:
        return False
