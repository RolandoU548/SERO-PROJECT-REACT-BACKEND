from flask import Blueprint
from flask import request, jsonify
import bcrypt
from models import db, InvitationClientForm
import re
from utils import APIException
import os

inviteClientForm = Blueprint("inviteClientForm", __name__)

@inviteClientForm.route("/inviteClientForm", methods=["POST"])
def create_hashClientForm():
        body = request.get_json()
        bhash_form = body.get("bhash_form")
        jsonify({"message": "A user must have at least one role"}), 400
        bhash_form = bytes(bhash_form, "utf-8")
        salt = bcrypt.gensalt(14)
        hashed_form = bcrypt.hashcf(bhash_form=bhash_form, salt=salt)
        invitation_clientForm = InvitationClientForm(
            invitation_hash=hashed_form.decode("utf-8"),
        )
        db.session.add(invitation_clientForm)
        db.session.commit()
        return jsonify({"message": "An client form has been created", "hashed_form": invitation_clientForm.invitation_hash}), 201
        return (
        jsonify(
            {
                "message": "Attributes name, lastname, email, password and roles are needed"
            }
        ),
        400,
    )