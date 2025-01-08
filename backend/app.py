from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import db, Task
from datetime import datetime
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Update with your database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure random key

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/')
def index():
    """Landing page."""
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    """Add a new task."""
    try:
        title = request.form['title']
        description = request.form['description']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        priority = request.form['priority']
        status = request.form['status']

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/update-task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    """Update an existing task."""
    task = Task.query.get_or_404(task_id)
    try:
        task.title = request.form['title']
        task.description = request.form['description']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task.priority = request.form['priority']
        task.status = request.form['status']

        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
