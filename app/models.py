from datetime import datetime, timezone
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # admin / manager / employee
    avatar_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assignee_id', back_populates='assignee', lazy='dynamic')
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by_id', back_populates='created_by', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='author', lazy='dynamic')
    attachments = db.relationship('Attachment', back_populates='uploader', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')
    watching = db.relationship('TaskWatcher', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low / medium / high / urgent
    status = db.Column(db.String(20), nullable=False, default='pending')   # pending / in_progress / review / completed / cancelled
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    estimated_hours = db.Column(db.Float, nullable=True)
    labels = db.Column(db.Text, nullable=True)  # comma-separated, e.g. "3D, Urgent, Client"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    assignee = db.relationship('User', foreign_keys=[assignee_id], back_populates='assigned_tasks')
    created_by = db.relationship('User', foreign_keys=[created_by_id], back_populates='created_tasks')
    comments = db.relationship('Comment', back_populates='task', lazy='dynamic', cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', back_populates='task', lazy='dynamic', cascade='all, delete-orphan')
    watchers = db.relationship('TaskWatcher', back_populates='task', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Task {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    task = db.relationship('Task', back_populates='comments')
    author = db.relationship('User', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id} on Task {self.task_id}>'


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    cloudinary_url = db.Column(db.String(500), nullable=False)
    cloudinary_public_id = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)   # bytes
    file_type = db.Column(db.String(100), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    task = db.relationship('Task', back_populates='attachments')
    uploader = db.relationship('User', back_populates='attachments')

    def __repr__(self):
        return f'<Attachment {self.filename}>'


class TaskWatcher(db.Model):
    __tablename__ = 'task_watchers'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    task = db.relationship('Task', back_populates='watchers')
    user = db.relationship('User', back_populates='watching')

    __table_args__ = (db.UniqueConstraint('task_id', 'user_id', name='uq_task_watcher'),)

    def __repr__(self):
        return f'<TaskWatcher task={self.task_id} user={self.user_id}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship('User', back_populates='notifications')
    task = db.relationship('Task')

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'
