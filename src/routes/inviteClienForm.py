from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, InvitationClientForm
import re
from utils import APIException
import os
import random

inviteclientform = Blueprint("inviteclientform", __name__)

@inviteclientform.route("/inviteclientform", methods=["POST"])
def create_hashClientForm():
        body = request.get_json()
        hash = random.getrandbits(128)
        invitation_clientForm = InvitationClientForm(
            invitation_hash=hash, expired_form=False
        )
        db.session.add(invitation_clientForm)
        db.session.commit()
        return jsonify({"message": "An client form has been created", "hashed_form": invitation_clientForm.serialize()}), 201
        