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
@app.route('/<string:library_name>')
def renderHome():
    return render_template('index.html')


@app.route('/<string:library_name>/books/<int:book_id>/')
def renderBook(library_name, book_id):
    try:
        item = session.query(Book).filter_by(id=book_id).one()
        return render_template('book.html', item=item)
    except:
        return notFound()


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
                        library_id=library_id,
                        category=request.form['category'],
                        cover=request.form['cover'])

        session.add(newEntry)
        session.commit()
        return redirect(url_for('renderLib', library_name=library_name))
    else:
        return render_template('addbook.html', library_name=library_name, library_id=library_id)


@app.route('/<string:library_name>/')
@app.route('/<string:library_name>/books/')
def renderLib(library_name):
    library = session.query(Library)
    items = session.query(Book)
    return render_template('books.html', items=items, library=library)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
