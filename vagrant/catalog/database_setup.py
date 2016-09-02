import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    category = Column(String(250), nullable=False)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    isbn = Column(String(2000), nullable=True)
    genre = Column(String(2000), nullable=False)
    description = Column(String(250), nullable=True)
    author = Column(String(1000), nullable=True)
    release = Column(String(1000), nullable=True)
    publisher = Column(String(1000), nullable=True)
    image = Column(String(5000), nullable=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    books = relationship(Books)


engine = create_engine("sqlite:///library.db")
Base.metadata.create_all(engine)
