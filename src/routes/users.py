from flask import Blueprint
from flask import request, jsonify

users= Blueprint('users', __name__)

@users.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200