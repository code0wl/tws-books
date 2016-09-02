from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book


app = Flask(__name__)

engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def renderHome():
    return render_template('index.html')


@app.route('/books')
def renderLib():
    library = session.query(Library)
    items = session.query(Book)
    return render_template('books.html', items=items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
