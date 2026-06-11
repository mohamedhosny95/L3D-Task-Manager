# Placeholder — implemented in Component 5
from app.admin import admin_bp

@admin_bp.route('/users')
def users():
    return 'Admin panel coming in Component 5'
