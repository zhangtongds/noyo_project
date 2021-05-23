from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from uuid import uuid1

from utils import generate_success_response, generate_error_response


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///person"
db = SQLAlchemy(app)


class Person(db.Model):
    """The person model."""

    __tablename__ = "person"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_latest = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, first_name, middle_name, last_name, email, age):
        self.user_id = user_id
        self.first_name = first_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    app.logger.info(f'Start to create user using data: {data}.')
    # TODO: Validate email.
    try:
        user_id = uuid1()
        print("create uuid:", user_id)
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

    new_user = Person(user_id, first_name, middle_name,
                      last_name, email, age)
    db.session.add(new_user)
    db.session.commit()
    success_response = generate_success_response(
        msg=f'User was successfully created.User id: {new_user.user_id}')
    return success_response


@app.route('/users/<id>')
def get_user(id):
    app.logger.info(f"Get user using user_id: {id}")
    user = Person.query.filter_by(user_id=id, is_latest=True).first()
    if not user:
        not_found_error = generate_error_response(
            404, "Not found", "User not found in db.")
        return not_found_error
    return jsonify({
        'user_id': user.user_id,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'email': user.email,
        'age': user.age,
    })


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    # user = Person.query.filter_by(user_id=id, is_latest=True).first()
    user = Person.query.filter_by(user_id=id).first()
    if not user:
        required_field_error = generate_error_response(
            msg=f"Cannot find user_id {id}.")
        return required_field_error

   
    

    first_name = data['first_name'] if 'first_name' in data else user.first_name
    middle_name = data['middle_name'] if 'middle_name' in data else user.middle_name
    last_name = data['last_name'] if 'last_name' in data else user.last_name
    email = data['email'] if 'email' in data else user.email
    age = data['age'] if 'age' in data else user.age

    new_user = Person(user.user_id, first_name, middle_name,
                      last_name, email, age)

    db.session.add(new_user)
    
    # Deactivate old user object.
    user.is_latest = False
    
    db.session.commit()

    return jsonify({
        'user_id': user.user_id,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'email': user.email,
        'age': user.age,
    })


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = Person.query.filter_by(user_id=id, is_latest=True).first()
    if not user:
        not_found_error = generate_error_response(
            404, "Not found", "User not found in db.")
        return not_found_error
    db.session.delete(user)
    db.session.commit()
    success_response = generate_success_response(
        msg='User was successfully deleted.')
    return success_response


@app.route('/users')
def get_users():
    return jsonify([
        {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'email': user.email,
            'age': user.age,
        } for user in Person.query.filter_by(is_latest=True).all()
    ])


if __name__ == '__main__':
    app.run(debug=True)
