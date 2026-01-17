from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

def can_edit_product(product) -> bool:
    if not current_user.is_authenticated:
        return False
    if getattr(current_user, "is_admin", False):
        return True
    return product.user_id == current_user.id  # owner-only

def require_can_edit_product(product):
    if not can_edit_product(product):
        abort(403)