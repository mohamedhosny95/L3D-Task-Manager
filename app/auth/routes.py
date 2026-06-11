# Placeholder — implemented in Component 3
from app.auth import auth_bp

@auth_bp.route('/login')
def login():
    return 'Login page coming in Component 3'

@auth_bp.route('/logout')
def logout():
    return 'Logout coming in Component 3'
