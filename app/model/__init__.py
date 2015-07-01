from structure import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://tang:a1a2a3a4@localhost/healthcare')
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


