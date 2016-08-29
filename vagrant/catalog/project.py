from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy


app = Flask(__name__)

engine = create_engine('sqlite:///shelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/shelters/<int:shelter_id>/')
def Shelters(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    items = session.query(Puppy).filter_by(shelter_id=shelter_id)
    output = ''
    for i in items:
        output += '<div class="item-list">'
        output += '<p>' + i.name + '</p>'
        output += '<p>' + i.dateOfBirth + '</p>'
        output += '<p>' + i.gender + '</p>'
        output += '</div>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

print(__name__)
