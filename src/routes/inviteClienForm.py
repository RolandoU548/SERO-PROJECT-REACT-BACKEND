from flask import Blueprint
from flask import jsonify
import bcrypt
from models import db, User, Role
import re
from utils import APIException
import os

inviteClientForm = Blueprint("inviteClientForm", __name__)

@inviteClientForm.route("/inviteClientForm", methods=["POST"])
bhash_form = get.body("bhash_form")
def create_hashClientForm():
            bhash_form = get.body("bhash_form")
            jsonify({"message": "A user must have at least one role"}), 400
            bhash_form = bytes(bhash_form, "utf-8")
            salt = bcrypt.gensalt(14)
            hashed_password = bcrypt.hashpw(bhash_form=bhash_form, salt=salt)