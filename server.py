from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4


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
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.version = version


@app.route("/user", methods=["POST"])
def add_user():
    data = request.get_json()
    app.logger.info(f"Start to create user using data: {data}.")

    try:
        user_id = uuid4()
        first_name = data["first_name"]
        middle_name = data.get("middle_name")
        last_name = data["last_name"]
        email = data["email"]
        age = data["age"]
        version = 0
        if len(first_name) < 1 or len(last_name) < 1 or len(email) < 1:
            missing_info_error_response = jsonify(
                {"message": "First_name or last_name or email field cannot be empty."})
            missing_info_error_response.status_code = 400
            return missing_info_error_response
    except KeyError:
        missing_info_error_response = jsonify(
            {"message": "First_name or last_name or email key is missing from request body."})
        missing_info_error_response.status_code = 400
        return missing_info_error_response

    new_user = Person(user_id, first_name, middle_name,
                      last_name, email, age, version)
    db.session.add(new_user)
    db.session.commit()
    created_response = jsonify(
        {"message": f"User was successfully created. User id: {new_user.user_id}"})
    created_response.status_code = 201
    return created_response


@app.route("/users/<id>", defaults={"version": None})
@app.route("/users/<id>/<version>")
def get_user(id, version):
    app.logger.info(
        f"Get the latest version {version} of user using user_id: {id}.")
    if not version:
        user = Person.query.filter_by(user_id=id, is_latest=True).first()
    else:
        user = Person.query.filter_by(user_id=id, version=version).first()
    if not user:
        not_found_error_response = jsonify(
            {"message": f"User {id} not found in db."})
        not_found_error_response.status_code = 404
        return not_found_error_response

    get_response = jsonify({
        "user_id": user.user_id,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "created_at": user.created_at,
        "is_latest": user.is_latest,
        "version": user.version
    })
    get_response.status_code = 200
    return get_response


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = Person.query.filter_by(user_id=id, is_latest=True).first()
    if not user:
        not_found_error_response = jsonify(
            {"message": f"User {id} not found in db."})
        not_found_error_response.status_code = 404
        return not_found_error_response

    if "user_id" in data:
        forbidden_response = jsonify(
            {"message": "Modifying user_id field is not allowed"})
        forbidden_response.status_code = 403
        return forbidden_response

    first_name = data["first_name"] if "first_name" in data else user.first_name
    middle_name = data["middle_name"] if "middle_name" in data else user.middle_name
    last_name = data["last_name"] if "last_name" in data else user.last_name
    email = data["email"] if "email" in data else user.email
    age = data["age"] if "age" in data else user.age
    version = user.version + 1

    new_user = Person(user.user_id, first_name, middle_name,
                      last_name, email, age, version)

    db.session.add(new_user)

    # Deactivate old user object.
    user.is_latest = False

    db.session.commit()
    put_response = jsonify({
        "user_id": new_user.user_id,
        "first_name": new_user.first_name,
        "middle_name": new_user.middle_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "age": new_user.age,
        "created_at": new_user.created_at,
        "is_latest": new_user.is_latest,
        "version": new_user.version
    })
    put_response.status_code = 200
    return put_response


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = Person.query.filter_by(user_id=id, is_latest=True).first()
    if not user:
        not_found_error_response = jsonify(
            {"message": f"User {id} not found in db."})
        not_found_error_response.status_code = 404
        return not_found_error_response
    db.session.delete(user)
    db.session.commit()
    success_response = jsonify(
        {"message": f"User {user.user_id} was successfully deleted."})
    success_response.status_code = 200
    return success_response


@app.route("/users")
def get_users():
    return jsonify([
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "created_at": user.created_at,
            "is_latest": user.is_latest,
            "version": user.version
        } for user in Person.query.filter_by(is_latest=True).all()
    ])


if __name__ == "__main__":
    app.run(debug=True)
