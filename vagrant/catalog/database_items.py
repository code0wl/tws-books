from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book
import datetime
import random
from random import randint
from sqlalchemy import asc


engine = create_engine('sqlite:///library.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add Shelters
library1 = Library(name="Hub")
session.add(library1)

book1 = Book(title="Java for dummies", isbn="isbn123",
             description="Some description", author="Some author",
             released="10-10-2010", category="Frontend", medium="file-pdf-o")

book2 = Book(title="In yo face", isbn="isbn123",
             description="Some description", author="Some author",
             released="10-10-2010", category="Frontend", medium="book")

session.add(book1)
session.add(book2)

session.commit()
