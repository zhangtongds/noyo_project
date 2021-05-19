from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import generate_success_response, generate_error_response


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///person"
db = SQLAlchemy(app)


class Person(db.Model):
    """The person model."""

    __tablename__ = "person"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, middle_name, last_name, email, age):
        self.first_name = first_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age
        

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    app.logger.info(f"Start to create user using data: {data}.")
    # TODO: Validate email.
    try:
        first_name = data['first_name']
        middle_name = data.get('middle_name')
        last_name = data['last_name']
        email = data['email']
        age = data['age']
        if len(first_name) < 1 or len(last_name) < 1 or len(email) < 1:
            missing_info_error = generate_error_response(
                msg="First_name or last_name or email field cannot be empty.")
            return missing_info_error
    except KeyError:
        print('try except')
        input_error = generate_error_response(
            msg="Missing first_name or last_name or email or age field.")
        return input_error

    new_user = Person(first_name, middle_name,
                      last_name, email, age)
    db.session.add(new_user)
    db.session.commit()
    success_response = generate_success_response(
        msg='User was successfully created.')
    return success_response


@app.route('/users/<id>')
def get_user(id):
    app.logger.info(f"Get user using user_id: {id}")
    person = Person.query.get(id)
    if not person:
        not_found_error = generate_error_response(
            404, "Not found", "User not found in db.")
        return not_found_error
    return {
        'user_id': person.user_id,
        'first_name': person.first_name,
        'middle_name': person.middle_name,
        'last_name': person.last_name,
        'email': person.email,
        'age': person.age,
    }


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    pass


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    person = Person.query.get(id)
    if not person:
        not_found_error = generate_error_response(
            404, "Not found", "User not found in db.")
        return not_found_error
    db.session.delete(person)
    db.session.commit()
    success_response = generate_success_response(
        msg='User was successfully deleted.')
    return success_response


@app.route('/users')
def get_users():
    return jsonify([
        {
            'user_id': person.user_id,
            'first_name': person.first_name,
            'middle_name': person.middle_name,
            'last_name': person.last_name,
            'email': person.email,
            'age': person.age,
        } for person in Person.query.all()
    ])


if __name__ == '__main__':
    app.run(debug=True)
