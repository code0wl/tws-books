from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book

app = Flask(__name__, static_folder='./node_modules')


engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def notFound():
    return render_template('404.html')


@app.route('/')
def renderHome():
    return render_template('index.html')


@app.route('/books/<string:library_name>/<int:book_id>/')
def renderBook(library_name, book_id):
    try:
        item = session.query(Book).filter_by(id=book_id).one()
        return render_template('book.html', item=item)
    except:
        return notFound()


@app.route('/books/<int:library_id>/new/', methods=['GET', 'POST'])
def newBook(library_id):
    if request.method == 'POST':
        newEntry = Book(description=request.form['description'],
                        title=request.form['title'],
                        medium=request.form['medium'],
                        isbn=request.form['isbn'],
                        author=request.form['author'],
                        released=request.form['released'],
                        publisher=request.form['publisher'],
                        book_id=book_id,
                        category=request.form['category'],
                        cover=request.form['cover'])

        library = session.query(Library)
        session.add(newEntry)
        session.commit()
        return redirect(url_for('renderLib', library_id=library_id))
    else:
        return render_template('addbook.html', library_id=library_id)


@app.route('/books/')
def renderLib():
    library = session.query(Library)
    items = session.query(Book)
    return render_template('books.html', items=items, library=library)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
