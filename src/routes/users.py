from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, User, Role
import re
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from utils import APIException
import os


def check_email(email):
    regex = r"[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,4}"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


users = Blueprint("users", __name__)


@users.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({"message": "User not found"}), 404


@users.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    email = get_jwt_identity()
    admin_found = False
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify("User has changed their email"), 404
    user = user.serialize()
    for role in user["role"]:
        if role["role"] == "admin":
            admin_found = True
            break
    if not admin_found:
        return jsonify("Unauthorized user"), 400
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200


@users.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()
    if (
        "email" in body.keys()
        and body["email"] != ""
        and body["email"] != None
        and "password" in body.keys()
        and body["password"] != ""
        and body["password"] is not None
        and "name" in body.keys()
        and body["name"] != ""
        and body["name"] is not None
        and "lastname" in body.keys()
        and body["lastname"] != ""
        and body["lastname"] is not None
        and "role" in body.keys()
        and body["role"] != ""
        and body["role"] is not None
    ):
        items = body.get("role", [])
        name = body.get("name").capitalize()
        lastname = body.get("lastname").capitalize()
        email = body.get("email").lower()
        password = body.get("password")
        possible_user = User.query.filter_by(email=email).first()
        if possible_user:
            return jsonify({"message": "User " + email + " already exists"}), 422
        if check_email(email) == False:
            return jsonify({"message": "Email format is invalid"}), 400
        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters"}), 400
        if len(items) < 1:
            return jsonify({"message": "A user must have at least one role"}), 400
        bpassword = bytes(password, "utf-8")
        salt = bcrypt.gensalt(14)
        hashed_password = bcrypt.hashpw(password=bpassword, salt=salt)
        roles = []
        for item in items:
            role = Role.query.filter_by(role=item).first()
            if role:
                roles.append(role)
            else:
                return jsonify({"message": f"Role {item} doesn't exist"}), 404
        user = User(
            name=name,
            lastname=lastname,
            email=email,
            password=hashed_password.decode("utf-8"),
        )
        user.role = roles
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "A user has been created", "email": user.email}), 201
    return (
        jsonify(
            {
                "message": "Attributes name, lastname, email, password and roles are needed"
            }
        ),
        400,
    )

@users.route("/user/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    body = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User {email} already exists"}), 422
    
    keys = ["name", "lastname", "email", "password"]
    for key in keys:
        if key in body and body[key] and body[key] != "":
            if key == "email":
                email = body[key].lower()
                if not check_email(email):
                    return jsonify({"message": "Email format is invalid"}), 400
                setattr(user, key, email)
            elif key == "password":
                if len(body[key]) < 6:
                    return jsonify({"message": "Password must be at least 6 characters"}), 400
                bpassword = bytes(body[key], "utf-8")
                salt = bcrypt.gensalt(14)
                hashed_password = bcrypt.hashpw(password=bpassword, salt=salt)
                setattr(user, key, hashed_password)
            else:
                setattr(user, key, body[key].capitalize())

    if "role" in body and body["role"] and body["role"] != "":
        items = body.get("role", [])
        if len(items) < 1:
            return jsonify({"message": "A user must have at least one role"}), 400
        roles = []
        for item in items:
            role = Role.query.filter_by(role=item).first()
            if role:
                roles.append(role)
            else:
                return jsonify({"message": f"Role {item} doesn't exist"}), 404
        user.role = roles
    db.session.commit()
    return jsonify({"message": "A user has been updated", "email": user.email}), 201


@users.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def deleteUser(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": user.email + " has been deleted"}), 200
    return jsonify({"message": "User not found"}), 404


@users.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email is None or password is None or email == "" or password == "":
        return {"message": "Parameters missing"}, 400
    user = User.query.filter_by(email=email.lower()).one_or_none()
    if user is None:
        return {"message": "User doesn't exist"}, 400
    password_byte = bytes(password, "utf-8")
    if bcrypt.checkpw(password_byte, user.password.encode("utf-8")):
        return {
            "message": "Token created",
            "token": create_access_token(identity=user.email),
        }, 200
    return {"message": "Incorrect password"}, 401
