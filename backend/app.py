from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')  # Default to 'production' if not set
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

# Initialize the database
db = SQLAlchemy(app)

# Import models (place this after initializing the app and db to avoid circular imports)
from models import Task, User

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{'id': t.id, 'title': t.title, 'description': t.description, 'due_date': t.due_date, 'priority': t.priority, 'status': t.status} for t in tasks]
    return jsonify(task_list)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        status=data.get('status')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully!', 'task': new_task.id}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully!'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'})

# Run the app
if __name__ == '__main__':
    # Use host '0.0.0.0' to allow access from outside the container if using Docker
    app.run(host='0.0.0.0', port=5000,debug=True)
