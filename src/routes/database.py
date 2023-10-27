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
    row = Row(
        text = json.dumps(body.get("text"))
        )
    db.session.add(row)
    db.session.commit()
    rows = Row.query.all()
    all_rows = list(map(lambda x: x.serialize(), rows))
    return jsonify(all_rows), 200

@database.route("/row/<int:row_id>", methods=["GET"])
def get_row(row_id):
    row = Row.query.get(row_id)
    return jsonify(row)

@database.route("/rows", methods=["GET"])
def get_rows():
    rows = Row.query.all()
    all_rows = list(map(lambda x: json.loads(x.serialize()["text"]), rows))
    return jsonify(all_rows), 200