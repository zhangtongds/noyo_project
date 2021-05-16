from flask import Flask, jsonify
from model import Person, connect_to_db
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def hello_world():
    person = Person.query.all()
    print(person)
    return 'hello world'


@app.route('/users/')
def get_users():
    return jsonify([
        {
            'id': user.user_id
        } for user in Person.query.all()
    ])


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run()
