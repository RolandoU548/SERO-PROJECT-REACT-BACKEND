from flask import Blueprint
from flask import request, jsonify
from models import db, Row
import re
from utils import APIException
import os
import json

database = Blueprint("database", __name__)

@database.route("/row", methods=["POST"])
def create_row():
    body = request.get_json()
    user = Row(
        text = json.dumps(body.get("text"))
        )
    db.session.add(user)
    db.session.commit()
    users = Row.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@database.route("/row/<int:row_id>", methods=["GET"])
def get_row(row_id):
    user = Row.query.get(row_id)
    if user:
        return jsonify(user.text), 200
    return jsonify({"message": "Row not found"}), 404
