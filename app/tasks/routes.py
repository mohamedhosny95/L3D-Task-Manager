# Placeholder — full implementation in Component 6 & 10
from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from app.tasks import tasks_bp


@tasks_bp.route('/')
def index():
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('tasks/dashboard.html')


@tasks_bp.route('/tasks')
@login_required
def task_list():
    return render_template('tasks/task_list.html')
