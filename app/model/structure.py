from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, BigInteger, ForeignKey, Enum, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy_fulltext import FullText, FullTextSearch
from ..helper import retrieve_subtitle, password_hash

Base = declarative_base()


class DiseaseHasSymptom(Base):
    __tablename__ = "Disease_Has_Symptom"
    disease_id = Column(Integer, ForeignKey('Disease.disease_id'), primary_key=True)
    symptom_id = Column(BigInteger, ForeignKey('Symptom.symptom_id'), primary_key=True)


class BodyLevel1(Base):
    __tablename__ = "Body_Level1"
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class BodyLevel2(Base):
    __tablename__ = "Body_Level2"
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    upper_level_id = Column(Integer, ForeignKey('Body_Level1.id'))
    upper_level = relationship("BodyLevel1")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "upper_level": self.upper_level.to_dict()}


class Disease(Base):
    __tablename__ = "Disease"
    disease_id = Column(Integer, primary_key=True, autoincrement=True)
    disease_name = Column(String(255))
    treatment = Column(Text)
    causes = Column(Text)
    prevention = Column(Text)
    description = Column(Text)
    possible_complications = Column(Text, name="possible complications")
    exams_and_tests = Column(Text, name="exams and tests")
    gender = Column(Enum("male", "female", "both"))
    body_part_1 = Column(SmallInteger, ForeignKey('Body_Level1.id'))
    body_part_2 = Column(SmallInteger, ForeignKey('Body_Level2.id'))

    level1 = relationship("BodyLevel1")
    level2 = relationship("BodyLevel2")
    symptoms = relationship("Symptom", secondary="Disease_Has_Symptom")

    def to_dict(self):
        symptoms_obj = []
        for symptom in self.symptoms:
            symptoms_obj.append(symptom.to_dict())
        
        return {"id": self.disease_id,
                "name": self.disease_name,
                "treatment": retrieve_subtitle(self.treatment),
                "causes": retrieve_subtitle(self.causes),
                "prevention": retrieve_subtitle(self.prevention),
                "description": retrieve_subtitle(self.description),
                "possible_complications": retrieve_subtitle(self.possible_complications),
                "exams_and_tests": retrieve_subtitle(self.exams_and_tests),
                "symptoms": symptoms_obj}


class Symptom(Base, FullText):
    __tablename__ = "Symptom"
    __fulltext_columns__ = ['symptom_name']
    symptom_id = Column(BigInteger, primary_key=True, autoincrement=True)
    symptom_name = Column(Text)
    symptom_type = Column(String(255))

    def to_dict(self):
        return {"id": self.symptom_id,
                "name": self.symptom_name,
                "type": self.symptom_type}


class User(Base):
    __tablename__ = "User"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)
    age = Column(SmallInteger)
    gender = Column(Enum("male", "female"))

    required = ["email", "password", "username"]

    def __init__(self, email, password, username, age=None, gender=None):
        if not email or not password:
            return
        self.email = email
        self.password = password_hash(password)
        self.username = username
        self.age = age
        self.gender = gender

    @classmethod
    def authentic(cls, session, email, password):
        hashed_password = password_hash(password)
        user = session.query(cls).filter(cls.email == email, cls.password == hashed_password).first()
        return user

    @classmethod
    def exist(cls, session, email):
        user = session.query(cls).filter(cls.email == email).first()
        return bool(user)

    def to_dict(self):
        return {"id": self.user_id,
                "email": self.email,
                "username": self.username,
                "password": self.password,
                "age": self.age,
                "gender": self.gender}

