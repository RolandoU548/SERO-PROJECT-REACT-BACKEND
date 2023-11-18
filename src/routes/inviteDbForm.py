from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, User, InvitationDatabaseForm, Row
import re
from utils import APIException
import os
import json
import random
from flask_jwt_extended import jwt_required, get_jwt_identity

invitedbform = Blueprint("invitedbform", __name__)

@invitedbform.route("/invitedbform", methods=["POST"])
@jwt_required()
def create_hashDbForm():
        body = request.get_json()
        clhash = random.getrandbits(128)
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first().id
        invitation_dbForm = InvitationDatabaseForm(
            invitation_hash=clhash, table_user_id = user, expired_form=False,
        )
        db.session.add(invitation_dbForm)
        db.session.commit()
        return jsonify({"message": "An client form has been created", "hashed_form": invitation_dbForm.serialize()}), 201

@invitedbform.route("/invitedbform/<clhash>", methods=["GET"])
def cols_hashDbForm(clhash):
    user = db.one_or_404(db.select(InvitationDatabaseForm).filter_by(invitation_hash=clhash)).table_user_id
    rows = Row.query.filter_by(user_id=user).first().text
    return jsonify({"sender_user_id": user, "columns": json.loads(rows)[0]}), 200

@invitedbform.route("/invitedbform/<clhash>", methods=["POST"])
def addRow_hashDbForm(clhash):
    body = request.get_json()
    invitation_capability = db.one_or_404(db.select(InvitationDatabaseForm).filter_by(invitation_hash=clhash))
    user = invitation_capability.table_user_id
    user_rows = Row.query.filter_by(user_id=user).first()
    if not user_rows:
        raise ValueError("Table already existed when invitation was given")
    
    user_rows_text = json.loads(user_rows.text)
    user_rows_text.append(body)

    user_rows.text = json.dumps(user_rows_text)
    db.session.commit()


    db.session.delete(invitation_capability)
    db.session.commit()

    user_rows = user_rows.serialize()
    user_rows["text"] = json.loads(user_rows["text"])
    return jsonify({"message": "Row updated", "info":user_rows}), 200
