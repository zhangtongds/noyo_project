from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from uuid import uuid4

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
    version = db.Column(db.Integer, nullable=False)
    is_latest = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, first_name, middle_name, last_name, email, age, version=0):
        self.user_id = user_id
        self.first_name = first_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.version = version


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    app.logger.info(f'Start to create user using data: {data}.')
    # TODO: Validate email.
    try:
        user_id = uuid4()
        first_name = data['first_name']
        middle_name = data.get('middle_name')
        last_name = data['last_name']
        email = data['email']
        age = data['age']
        version = 0
        if len(first_name) < 1 or len(last_name) < 1 or len(email) < 1:
            missing_info_error = generate_error_response(
                msg="First_name or last_name or email field cannot be empty.")
            return missing_info_error
    except KeyError:
        input_error = generate_error_response(
            msg="Missing first_name or last_name or email or age field.")
        return input_error

    new_user = Person(user_id, first_name, middle_name,
                      last_name, email, age, version)
    db.session.add(new_user)
    db.session.commit()
    success_response = generate_success_response(
        msg=f'User was successfully created.User id: {new_user.user_id}')
    return success_response


@app.route('/users/<id>', defaults={'version': None})
@app.route('/users/<id>/<version>')
def get_user(id, version):
    app.logger.info(f"Get user using user_id: {id} {version}")
    if not version:
        user = Person.query.filter_by(user_id=id, is_latest=True).first()
    else:
        user = Person.query.filter_by(user_id=id, version=version).first()
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
        'created_at': user.created_at,
        'is_latest': user.is_latest,
        'version': user.version
    })


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = Person.query.filter_by(user_id=id, is_latest=True).first()
    if not user:
        required_field_error = generate_error_response(
            404, "Not found", f"Cannot find user using user_id {id}.")
        return required_field_error

    if 'user_id' in data:
        id_field_error = generate_error_response(
            403, "Forbidden", f"Cannot modify user_id field.")
        return id_field_error
    
    first_name = data['first_name'] if 'first_name' in data else user.first_name
    middle_name = data['middle_name'] if 'middle_name' in data else user.middle_name
    last_name = data['last_name'] if 'last_name' in data else user.last_name
    email = data['email'] if 'email' in data else user.email
    age = data['age'] if 'age' in data else user.age
    version = user.version + 1

    new_user = Person(user.user_id, first_name, middle_name,
                      last_name, email, age, version)

    db.session.add(new_user)

    # Deactivate old user object.
    user.is_latest = False

    db.session.commit()

    return jsonify({
        'user_id': new_user.user_id,
        'first_name': new_user.first_name,
        'middle_name': new_user.middle_name,
        'last_name': new_user.last_name,
        'email': new_user.email,
        'age': new_user.age,
        'created_at': new_user.created_at,
        'is_latest': new_user.is_latest,
        'version': new_user.version
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
        msg=f'User {user.user_id} was successfully deleted.')
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
