from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, InvitationClientForm
import re
from utils import APIException
import os
import random
from flask_jwt_extended import jwt_required

inviteclientform = Blueprint("inviteclientform", __name__)

@inviteclientform.route("/inviteclientform", methods=["POST"])
@jwt_required()
def create_hashClientForm():
        body = request.get_json()
        clhash = random.getrandbits(128)
        invitation_clientForm = InvitationClientForm(
            invitation_hash=clhash, expired_form=False
        )
        db.session.add(invitation_clientForm)
        db.session.commit()
        return jsonify({"message": "An client form has been created", "hashed_form": invitation_clientForm.serialize()}), 201

@inviteclientform.route("/inviteclientform/<clhash>", methods=["GET"])
def exists_hashClientForm(clhash):
    db.one_or_404(db.select(InvitationClientForm).filter_by(invitation_hash=clhash))
    return jsonify({"message": "Exists"}), 200
