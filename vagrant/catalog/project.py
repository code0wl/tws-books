from flask import Flask, render_template, request, redirect, url_for, jsonify,\
    flash, session as login_session, make_response
from sqlalchemy import create_engine
import random
import string
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Library, Book
from werkzeug.utils import secure_filename

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

UPLOAD_FOLDER = './media/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='../catalog')

engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "twsbooks"


# General 404 page
def notFound():
    return render_template('404.html')


# Render home
@app.route('/')
def renderHome():
    return render_template('index.html')


# Render login
@app.route('/<string:library_name>/login/')
def showLogin(library_name):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    fragment = 'https://accounts.google.com/o/oauth2/revoke?token='
    url = fragment + '%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Render a single book
@app.route('/<string:library_name>/books/<int:book_id>/')
def renderBook(library_name, book_id):
    try:
        item = session.query(Book).filter_by(id=book_id).one()
        return render_template('book.html', item=item,
                               library_name=library_name)
    except:
        return notFound()


# Create a book entry
@app.route('/<string:library_name>/<int:library_id>/books/new/',
           methods=['GET', 'POST'])
def newBook(library_name, library_id):
    if 'user_name' not in login_session:
        return redirect(url_for('showLogin', library_name=library_name))
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
        return render_template('addbook.html', library_name=library_name,
                               library_id=library_id)


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
def bookEntryJSON(library_name, book_id):
    entry = session.query(Book).filter_by(id=book_id).one()
    return jsonify(entry=entry.serialize)


# Remove a book
@app.route('/<string:library_name>/books/<int:book_id>/remove',
           methods=['GET', 'POST'])
def deleteBook(library_name, book_id):
    if 'user_name' not in login_session:
        return redirect(url_for('showLogin', library_name=library_name))
    entry = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(entry)
        session.commit()
        return redirect(url_for('getLib', library_name=library_name))
    else:
        return render_template('remove.html', item=entry,
                               library_name=library_name)


# Check to see if input value exist and edit them accordingly
@app.route('/<string:library_name>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(library_name, book_id):
    if 'user_name' not in login_session:
        return redirect(url_for('showLogin', library_name=library_name))
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
        return render_template('edit-book.html', item=entry,
                               library_name=library_name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print __name__
