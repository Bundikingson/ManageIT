from flask import Flask, render_template, request, redirect, url_for
from models import db, Task  # Import db and Task model

app = Flask(__name__)

# Configure the app to use SQLite for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Path to your database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save memory
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize the database with the Flask app
db.init_app(app)

# Create the database tables (if they don't exist already)
with app.app_context():
    db.create_all()  # Creates the tables in the database

@app.route('/')
def index():
    tasks = Task.query.all()  # Retrieve all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:task_id>')
def view_task(task_id):
    task = Task.query.get_or_404(task_id)  # Retrieve the task with the given ID
    return render_template('tasks.html', task=task)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Get the form data
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']

        # Create a new task instance
        new_task = Task(title=title, description=description, due_date=due_date, status=status)

        # Add the task to the session and commit the changes
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to the task list

    return render_template('create_task.html')  # Render the task creation form

@app.route('/task/<int:task_id>/delete')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Retrieve the task to delete
    db.session.delete(task)  # Delete the task from the session
    db.session.commit()  # Commit the change to the database
    return redirect(url_for('index'))  # Redirect to the task list

if __name__ == "__main__":
    app.run(debug=True)
