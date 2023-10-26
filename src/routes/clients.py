from flask import Blueprint
from flask import request, jsonify
from models import db, Client
from utils import APIException
import os
import json

clients = Blueprint("clients", __name__)

# Get todos los clientes


@clients.route("/clients", methods=["GET"])
def get_all_clients():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients]), 200


# Crear un nuevo cliente
@clients.route("/clients", methods=["POST"])
def create_client():
    data = request.form
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    new_client = Client(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        image=filename,
        business=data["business"],
        description=data["description"],
        status=data["status"]
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.serialize()), 201

# Actualizar un cliente


@clients.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    data = request.get_json()
    client.name = data["name"]
    client.email = data["email"]
    client.phone = data["phone"]
    client.image = data["image"]
    client.business = data["business"]
    client.description = data["description"]
    client.status = data["status"]
    db.session.commit()
    return jsonify(client.serialize()), 200

# Eliminar un cliente


@clients.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"}), 200