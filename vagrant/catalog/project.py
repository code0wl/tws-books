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


@app.route('/books/<int:book_id>/')
def renderBook(book_id):
    try:
        item = session.query(Book).filter_by(id=book_id).one()
        return render_template('book.html', item=item)
    except:
        return notFound()


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(book_id):
    if request.method == 'POST':
        newItem = Book(
            title=request.form['name'], book_id=book_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('renderBook', book_id=book_id))
    else:
        return render_template('addbook.html', book_id=book_id)


@app.route('/books/')
def renderLib():
    items = session.query(Book)
    return render_template('books.html', items=items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
