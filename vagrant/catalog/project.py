from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy


app = Flask(__name__)

engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def Library():
    shelter = session.query(Books)
    items = session.query(Book)
    output = ''
    for i in items:
        output += '<div style="background: #f0f0f0; margin: 1rem;">'
        output += '<p>' + i + '</p>'
        output += '</div>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print(__name__)
