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
library1 = Library(name="Knowledge Hub")
session.add(library1)

book1 = Book(title="Java for dummies", isbn="isbn123",
             description="Some description", author="Some author",
             released="10-10-2010", category="Frontend")
session.add(book1)

session.commit()
