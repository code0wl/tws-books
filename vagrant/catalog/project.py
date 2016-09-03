from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session as login_session
from sqlalchemy import create_engine
import random
import string
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './media/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='../catalog')

engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def notFound():
    return render_template('404.html')


# Render home
@app.route('/')
def renderHome():
    return render_template('index.html')


# generate token
state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))

# Render login
@app.route('/<string:library_name>/login/')
def getLogin(library_name):

    login_session['state'] = state
    return "The current session state is %s" % login_session['state']


# Render a single book
@app.route('/<string:library_name>/books/<int:book_id>/')
def renderBook(library_name, book_id):
    try:
        item = session.query(Book).filter_by(id=book_id).one()
        return render_template('book.html', item=item, library_name=library_name)
    except:
        return notFound()


# Create a book entry
@app.route('/<string:library_name>/<int:library_id>/books/new/', methods=['GET', 'POST'])
def newBook(library_name, library_id):
    if request.method == 'POST':
        newEntry = Book(description=request.form['description'],
                        title=request.form['title'],
                        medium=request.form['medium'],
                        isbn=request.form['isbn'],
                        author=request.form['author'],
                        released=request.form['released'],
                        publisher=request.form['publisher'],
                        category=request.form['category'],
                        cover=request.form['cover'])

        session.add(newEntry)
        session.commit()
        return redirect(url_for('getLib', library_name=library_name))
    else:
        return render_template('addbook.html', library_name=library_name, library_id=library_id)


# Query books
@app.route('/<string:library_name>/')
@app.route('/<string:library_name>/books/')
def getLib(library_name):
    library = session.query(Library)
    items = session.query(Book)
    return render_template('books.html', items=items, library=library)


# API for books
@app.route('/<string:library_name>/books/JSON/')
def getBookJSON(library_name):
    items = session.query(Book)
    return jsonify(Books=[i.serialize for i in items])


# API for a specific book
@app.route('/<string:library_name>/books/<int:book_id>/JSON/')
def menuItemJSON(library_name, book_id):
    entry = session.query(Book).filter_by(id=book_id).one()
    return jsonify(entry=entry.serialize)


# Remove a book
@app.route('/<string:library_name>/books/<int:book_id>/remove', methods=['GET', 'POST'])
def deleteBook(library_name, book_id):
    entry = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(entry)
        session.commit()
        return redirect(url_for('getLib', library_name=library_name))
    else:
        return render_template('remove.html', item=entry, library_name=library_name)


# Check to see if input value exist and edit them accordingly
@app.route('/<string:library_name>/books/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(library_name, book_id):
    entry = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['title']:
            entry.title = request.form['title']
        if request.form['description']:
            entry.description = request.form['description']
        if request.form['author']:
            entry.author = request.form['author']
        if request.form['category']:
            entry.category = request.form['category']
        if request.form['released']:
            entry.released = request.form['released']
        if request.form['medium']:
            entry.medium = request.form['medium']
        if request.form['cover']:
            entry.cover = request.form['cover']
        if request.form['isbn']:
            entry.isbn = request.form['isbn']
        session.add(entry)
        session.commit()
        return redirect(url_for('getLib', library_name=library_name))
    else:
        return render_template('edit-book.html', item=entry, library_name=library_name)


if __name__ == '__main__':
    app.secret_key = state
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
