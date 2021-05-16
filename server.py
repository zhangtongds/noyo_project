from flask import Flask, jsonify, request
from model import db, Person, connect_to_db
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def hello_world():
    person = Person.query.all()
    print(person)
    return 'hello world'


@app.route('/persons')
def get_users():
    return jsonify([
        {
            'id': user.user_id
        } for user in Person.query.all()
    ])


@app.route('/person', methods=['POST'])
def add_person():
    user_id = request.json.get('user_id')
    first_name = request.json.get('first_name')
    middle_name = request.json.get('middle_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    age = request.json.get('age')
    new_person = Person(user_id, first_name, middle_name,
                        last_name, email, age)
    db.session.add(new_person)
    db.session.commit()

    return {'status': 200}


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run()
