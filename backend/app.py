from flask import Flask, jsonify, request
from models import Task
from routes import task_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(task_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
