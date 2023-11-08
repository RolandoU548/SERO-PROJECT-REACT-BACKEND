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
    data = request.get_json()
    name = data.get("name")
    lastname = data.get("lastname")
    email = data.get("email")
    phone = data.get("phone")
    image = data.get("image")
    business = data.get("business")
    description = data.get("description")
    status = data.get("status")
    if not name or not email or not phone or not image or not business or not description or not status or not lastname:
        return jsonify({"message": "Missing required fields"}), 400
    client = Client(name=name, email=email, phone=phone, image=image,
                     business=business, description=description, status=status, lastname=lastname)
    db.session.add(client)
    db.session.commit()
    return jsonify(client.serialize()), 201


# Actualizar un cliente

@clients.route("/clients/<int:client_id>", methods=["PUT"])
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
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"}), 200