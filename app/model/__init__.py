from structure import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_fulltext import FullTextSearch, FullTextMode

import os

if os.getenv("COMPUTERNAME") == "ALSTON-TABLET":
    engine = create_engine('mysql://root@127.0.0.1/healthcare')
else:
    engine = create_engine('mysql://tang:a1a2a3a4@localhost/healthcare')
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


