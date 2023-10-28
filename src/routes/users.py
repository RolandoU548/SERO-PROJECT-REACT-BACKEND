from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, User
import re
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from utils import APIException
import os


def check_email(email):
    regex = r'[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,4}'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False


users = Blueprint("users", __name__)


@users.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200


@users.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({"message": "User not found"}), 404


@users.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()
    if "email" in body.keys() and body["email"] != "" and "password" in body.keys() and body["password"] != "" and "name" in body.keys() and body["name"] != "" and "lastname" in body.keys() and body["lastname"] != "":
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
        bpassword = bytes(password, "utf-8")
        salt = bcrypt.gensalt(14)
        hashed_password = bcrypt.hashpw(password=bpassword, salt=salt)
        user = User(
            name=name,
            lastname=lastname,
            email=email,
            password=hashed_password.decode("utf-8")
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "A user has been created",
            "email": user.email
        }), 201
    return jsonify({
        "message": "Attributes name, lastname, email and password are needed"
    }), 400


@users.route("/user", methods=["DELETE"])
@jwt_required()
def deleteUser():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
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
        return {"message": "Token created", "token": create_access_token(identity=user.email)}, 200
    return {"message": "Incorrect password"}, 401

