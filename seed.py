"""
Run with: flask shell < seed.py  OR  python seed.py
Creates the default admin user: admin@lancer3d.com / admin123
"""
import os
from app import create_app, db
from app.models import User
from bcrypt import hashpw, gensalt

app = create_app(os.environ.get('FLASK_ENV', 'production'))

with app.app_context():
    existing = User.query.filter_by(email='admin@lancer3d.com').first()
    if existing:
        print('Admin user already exists — skipping.')
    else:
        pw_hash = hashpw('admin123'.encode('utf-8'), gensalt()).decode('utf-8')
        admin = User(
            name='Admin',
            email='admin@lancer3d.com',
            password_hash=pw_hash,
            role='admin',
            is_active=True,
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created: admin@lancer3d.com / admin123')
