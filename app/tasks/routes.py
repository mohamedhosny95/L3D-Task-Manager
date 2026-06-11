# Placeholder — implemented in Component 6
from flask import redirect, url_for
from app.tasks import tasks_bp

@tasks_bp.route('/')
def index():
    return redirect(url_for('tasks.dashboard'))

@tasks_bp.route('/dashboard')
def dashboard():
    return 'Dashboard coming in Component 10'

@tasks_bp.route('/tasks')
def task_list():
    return 'Task list coming in Component 6'
