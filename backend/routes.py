from flask import Blueprint, request, jsonify
from models import Task

task_routes = Blueprint('task_routes', __name__)

tasks = []

# GET /tasks - Retrieve all tasks
@task_routes.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks])

# POST /tasks - Add a new task
@task_routes.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = Task(data['title'], data['description'])
    tasks.append(task)
    return jsonify(task.to_dict()), 201

# PUT /tasks/{id} - Update a task
@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = tasks[id]
    task.update(data['title'], data['description'])
    return jsonify(task.to_dict())

# DELETE /tasks/{id} - Delete a task
@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = tasks.pop(id)
    return jsonify(task.to_dict())
