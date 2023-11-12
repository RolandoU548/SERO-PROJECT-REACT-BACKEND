from flask import Blueprint
from flask import request, jsonify
from models import db, Client, InvitationClientForm
from utils import APIException
import os
import json
from flask_jwt_extended import jwt_required

clients = Blueprint("clients", __name__)

# Get todos los clientes


@clients.route("/clients", methods=["GET"])
@jwt_required()
def get_all_clients():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients]), 200


def create_client_common(client):
    name = client.get("name")
    lastname = client.get("lastname")
    email = client.get("email")
    phone = client.get("phone")
    image = client.get("image")
    business = client.get("business")
    description = client.get("description")
    status = client.get("status")
    if not name or not email or not phone or not image or not business or not description or not status or not lastname:
        return jsonify({"message": "Missing required fields"}), 400
    client = Client(name=name, email=email, phone=phone, image=image,
                     business=business, description=description, status=status, lastname=lastname)
    db.session.add(client)
    db.session.commit()
    return jsonify(client.serialize()), 201


# Crear un nuevo cliente
@clients.route("/clients", methods=["POST"])
@jwt_required()
def create_client():
    client = request.get_json()
    return create_client_common(client)


# Crear un nuevo cliente (sin iniciar sesión, usando el invitation form hash)
@clients.route("/clients_with_clhash", methods=["POST"])
def create_client_with_clhash():
    data = request.get_json()
    clhash = data.get("clhash")
    client = data.get("client")
    invitation_capability = db.one_or_404(db.select(InvitationClientForm).filter_by(invitation_hash=clhash))
    result = create_client_common(client)
    db.session.delete(invitation_capability)
    db.session.commit()
    return result


# Actualizar un cliente

@clients.route("/clients/<int:client_id>", methods=["PUT"])
@jwt_required()
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    data = request.get_json()
    client.name = data["name"]
    client.lastname = data["lastname"]
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
@jwt_required()
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"}), 200