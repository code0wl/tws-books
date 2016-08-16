import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Shelter(Base):
    __tablename__ = "shelter"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(500))
    state = Column(String(500))
    zipCode = Column(String(500))
    website = Column(String(500), nullable=True)


class Puppy(Base):
    __tablename__ = "puppy"
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    dateOfBirth = Column(String(1000))
    picture = Column(String(5000), nullable=True)
    gender = Column(String(50), nullable=False)
    weight = Column(Integer, nullable=False)
    shelter_id = Column(Integer, ForeignKey("shelter.id"))
    shelter = relationship(Shelter)


engine = create_engine("sqlite:///shelter.db")
Base.metadata.create_all(engine)
