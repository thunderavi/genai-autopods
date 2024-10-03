# routes/task_routes.py

from flask import Blueprint, request, jsonify

# Initialize a Flask blueprint for tasks
task_bp = Blueprint('task_bp', __name__)

# Example task endpoint (you can modify as needed)
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"message": "This endpoint will return tasks."}), 200
