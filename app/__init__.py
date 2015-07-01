reload(__import__('sys')).setdefaultencoding('utf-8')
from flask import Flask

app = Flask(__name__)

from app import views
