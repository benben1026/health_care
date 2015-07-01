from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

Disease_Has_Symptom = Table('Disease_Has_Symptom', Base.metadata,
        Column('disease_id', Integer, ForeignKey('Disease.disease_id')),
        Column('symptom_id', BigInteger, ForeignKey('Symptom.symptom_id'))
)

class Disease(Base):
    __tablename__ = "Disease"
    disease_id = Column(Integer, primary_key=True)
    disease_name = Column(String(255))
    treatment = Column(Text)
    causes = Column(Text)
    prevention = Column(Text)
    description = Column(Text)
    symptoms = relationship("Symptom", secondary=Disease_Has_Symptom)

    def to_dict(self):
        symptoms_obj = []
        for symptom in self.symptoms:
            symptoms_obj.append(symptom.to_dict())
        
        return {"id": self.disease_id,
                "name": self.disease_name,
                "treatment": self.treatment,
                "causes": self.causes,
                "prevention": self.prevention,
                "description": self.description,
                "symptoms": symptoms_obj}

class Symptom(Base):
    __tablename__ = "Symptom"
    symptom_id = Column(BigInteger, primary_key=True)
    symptom_name = Column(Text)
    symptom_type = Column(String(255))

    def to_dict(self):
        return {"id": self.symptom_id,
                "name": self.symptom_name,
                "type": self.symptom_type}
