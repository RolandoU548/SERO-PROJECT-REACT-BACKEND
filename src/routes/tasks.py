from models import db, Task
from flask import Blueprint, request, jsonify
from utils import APIException


tasks = Blueprint("tasks", __name__)

# GET todas las tareas
@tasks.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.serialize() for t in tasks]), 200

# POST nueva tarea
@tasks.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        raise APIException('No input data provided', status_code=400)
    try:
        task = Task(
            text=data['text'],
            completed=False,
            date=data['date']
        )
        
        db.session.add(task)
        db.session.commit()
        return jsonify(task.serialize()), 201
    except KeyError as e:
        raise APIException(f'Missing required field: {e}', status_code=400)

# PUT marcar tarea como completada
@tasks.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        raise APIException('Task not found', status_code=404)
    data = request.get_json()
    task.completed = data['completed']
    db.session.commit()
    return jsonify(task.serialize()), 200

# DELETE eliminar una tarea
@tasks.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        raise APIException('Task not found', status_code=404)
    db.session.delete(task)
    db.session.commit()
    return '', 204
