from flask import Blueprint
from flask import request, jsonify
from models import db, Row, User
import re
from utils import APIException
import os
import json
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

database = Blueprint("database", __name__)

@database.route("/row", methods=["POST"])
@jwt_required()
def create_row():
    body = request.get_json()
    user_id = User.query.filter_by(email=get_jwt_identity()).first().id
    user_rows = Row.query.filter_by(user_id=user_id).first()
    if user_rows:
        user_rows.text = json.dumps(body.get("text"))
        db.session.commit()
        user_rows = user_rows.serialize()
        user_rows["text"] = json.loads(user_rows["text"])
        return jsonify({"message": "Row updated", "info":user_rows}), 200
    row = Row(
        user_id = user_id,
        text = json.dumps(body.get("text"))
        )
    db.session.add(row)
    db.session.commit()
    rows = Row.query.all()
    all_rows = list(map(lambda x: x.serialize(), rows))
    return jsonify({"message": "Row created", "info": all_rows}), 200

@database.route("/row/<int:row_id>", methods=["GET"])
@jwt_required()
def get_row(row_id):
    row = Row.query.get(row_id)
    if row:
        row = row.serialize()
        row["text"] = json.loads(row["text"])
        return jsonify({"message":"Row found", "info": row}), 200
    return jsonify({"message": "Row not found"}), 404

@database.route("/user_rows", methods=["GET"])
@jwt_required()
def get_user_rows():
    user_rows = Row.query.filter_by(user_id=User.query.filter_by(email=get_jwt_identity()).first().id).first()
    if user_rows:
        user_rows = user_rows.serialize()
        user_rows["text"] = json.loads(user_rows["text"])
        return jsonify({"message": f"{get_jwt_identity()} rows", "info": user_rows}), 200
    return jsonify({"message": f"User {get_jwt_identity()} doesn't have any rows saved"}), 404

@database.route("/rows", methods=["GET"])
@jwt_required()
def get_rows():
    rows = Row.query.all()
    all_rows = list(map(lambda x: json.loads(x.serialize()["text"]), rows))
    return jsonify({"message": "All rows","info": all_rows}), 200
