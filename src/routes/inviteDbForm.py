from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, InvitationDatabaseForm
import re
from utils import APIException
import os
import random
from flask_jwt_extended import jwt_required

invitedbform = Blueprint("invitedbform", __name__)

@invitedbform.route("/invitedbform", methods=["POST"])
@jwt_required()
def create_hashDbForm():
        body = request.get_json()
        clhash = random.getrandbits(128)
        invitation_dbForm = InvitationDatabaseForm(
            invitation_hash=clhash, expired_form=False
        )
        db.session.add(invitation_dbForm)
        db.session.commit()
        return jsonify({"message": "An client form has been created", "hashed_form": invitation_dbForm.serialize()}), 201

@invitedbform.route("/invitedbform/<clhash>", methods=["GET"])
def exists_hashDbForm(clhash):
    db.one_or_404(db.select(InvitationDatabaseForm).filter_by(invitation_hash=clhash))
    return jsonify({"message": "Exists"}), 200
