
from flask import Blueprint
from flask import request, jsonify
from models import db, Suggestion
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils import APIException
import re
import os

def check_email(email):
    regex = r"[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,4}"
    if re.fullmatch(regex, email):
        return True
    else:
        return False

user_suggestion = Blueprint("user_suggestion", __name__)


@user_suggestion.route("/suggestions", methods=["GET"])
@jwt_required()
def get_suggestions():
    suggestions = Suggestion.query.all()
    all_suggestions = list(map(lambda suggestion: suggestion.serialize(), suggestions))
    return jsonify(all_suggestions), 200


@user_suggestion.route("/suggestion", methods=["POST"])
def create_suggestion():
    body = request.get_json()
    if (
        "name" in body.keys()
        and body["name"] != ""
        and body["name"] is not None
        and "email" in body.keys()
        and body["email"] != ""
        and body["email"] != None
        and "text" in body.keys()
        and body["text"] != ""
        and body["text"] is not None
    ):
        name = body.get("name").capitalize()
        text = body.get("text").capitalize()
        email = body.get("email").lower()
        if check_email(email) == False:
            return jsonify({"message": "Email format is invalid"}), 400
        suggestion = Suggestion(name=name, email=email, text=text)
        db.session.add(suggestion)
        db.session.commit()
        return (
            jsonify({"message": "A suggestion has been saved", "email": suggestion.email}),
            200,
        )
    return (
        jsonify({"message": "Attributes name, email and text are needed"}),
        400,
    )

@user_suggestion.route("/suggestion/<int:suggestion_id>", methods=["DELETE"])
@jwt_required()
def deleteSuggestion(suggestion_id):
    suggestion = Suggestion.query.get(suggestion_id)
    if suggestion:
        db.session.delete(suggestion)
        db.session.commit()
        return jsonify({"message": suggestion.email + " has been deleted"}), 200
    return jsonify({"message": "Suggestion not found"}), 404