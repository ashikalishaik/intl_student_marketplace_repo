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

def can_edit_product(product):
    if not current_user.is_authenticated:
        return False
    # admin can edit all
    if current_user.is_admin():
        return True
    # seller can edit only their own product
    return product.seller_id == current_user.id

def require_can_edit_product(product):
    if not can_edit_product(product):
        abort(403)


def can_view_order(order):
    """Order is viewable by the buyer or by an admin."""
    if not current_user.is_authenticated:
        return False
    if current_user.is_admin():
        return True
    return getattr(order, "buyer_id", None) == current_user.id


def require_can_view_order(order):
    if not can_view_order(order):
        abort(403)