from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wfh.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref='assignee', lazy=True)
    time_entries = db.relationship('TimeEntry', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.String(200))

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    tasks = Task.query.filter_by(assignee_id=current_user.id).all()
    time_entries = TimeEntry.query.filter_by(user_id=current_user.id).all()
    meetings = Meeting.query.filter_by(organizer_id=current_user.id).all()
    return render_template('dashboard.html', 
                         tasks=tasks, 
                         time_entries=time_entries, 
                         meetings=meetings)

@app.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.filter_by(assignee_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/time-tracking')
@login_required
def time_tracking():
    entries = TimeEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('time_tracking.html', entries=entries)

@app.route('/meetings')
@login_required
def meetings():
    meetings = Meeting.query.filter_by(organizer_id=current_user.id).all()
    return render_template('meetings.html', meetings=meetings)

@app.route('/community')
@login_required
def community():
    return render_template('community.html')

# API Routes
@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status='pending',
        priority=data['priority'],
        assignee_id=current_user.id,
        due_date=datetime.fromisoformat(data['due_date'])
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

@app.route('/api/time-entries', methods=['POST'])
@login_required
def start_time_entry():
    entry = TimeEntry(
        user_id=current_user.id,
        start_time=datetime.utcnow(),
        description=request.json.get('description', '')
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'message': 'Time tracking started'})

@app.route('/api/meetings', methods=['POST'])
@login_required
def create_meeting():
    data = request.json
    meeting = Meeting(
        title=data['title'],
        description=data['description'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        organizer_id=current_user.id
    )
    db.session.add(meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting scheduled successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)