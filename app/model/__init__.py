from structure import *
#from pubmed import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_fulltext import FullTextSearch, FullTextMode

import os

engine = create_engine('mysql://healthcare:sf4e5UcjjFhy8u2z@128.199.82.15/healthcare')
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


