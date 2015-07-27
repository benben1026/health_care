reload(__import__('sys')).setdefaultencoding('utf-8')
from flask import Flask


app = Flask(__name__)
app.secret_key = "C-U-H-K-2000"

from app import views
