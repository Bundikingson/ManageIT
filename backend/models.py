from app import db
from datetime import datetime

# Task model definition
class Task(db.Model):
    __tablename__ = 'tasks'  # Name of the table in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)  # Task title (required field)
    description = db.Column(db.Text, nullable=True)  # Task description (optional field)
    due_date = db.Column(db.DateTime, nullable=False)  # Task due date (required field)
    priority = db.Column(db.String(50), nullable=False)  # Task priority (required field)
    status = db.Column(db.String(50), nullable=False)  # Task status (required field)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set the creation date
    
    # Optional: relationship with the User model (if you need to assign tasks to users)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # user = db.relationship('User', back_populates='tasks')
    
    def __repr__(self):
        return f"<Task {self.title}, Status: {self.status}>"

# User model definition (if users are needed in your system)
class User(db.Model):
    __tablename__ = 'users'  # Name of the table in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(100), unique=True, nullable=False)  # Unique username (required field)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email (required field)
    password = db.Column(db.String(100), nullable=False)  # User password (required field)
    
    # Relationship with Task model (if a user can have multiple tasks)
    tasks = db.relationship('Task', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.username}>"

# Make sure to initialize the database after creating this file:
# Use the following in a Flask shell or another script:
# from app import db
# db.create_all()
