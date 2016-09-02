import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Library(Base):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True)
    name = Column(String(5000), nullable=False)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String(5000), nullable=True)
    medium = Column(String(100), nullable=False)
    isbn = Column(String(2000), nullable=True)
    description = Column(String(250), nullable=True)
    author = Column(String(1000), nullable=True)
    released = Column(String(1000), nullable=True)
    publisher = Column(String(1000), nullable=True)
    cover = Column(String(5000), nullable=True)
    category = Column(String(2000), nullable=False)
    book_id = Column(Integer, ForeignKey("library.id"))
    books = relationship(Library)


engine = create_engine("sqlite:///library.db")
Base.metadata.create_all(engine)
