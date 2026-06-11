# Placeholder — full implementation in Component 5
from flask_login import login_required
from app.admin import admin_bp
from app.decorators import role_required


@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    return 'Admin panel — coming in Component 5'
