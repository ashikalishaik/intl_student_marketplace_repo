from datetime import datetime
from ..extensions import db

class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

class CartItem(db.Model):
    __tablename__ = "cart_items"
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    qty = db.Column(db.Integer, default=1, nullable=False)

    cart = db.relationship("Cart", lazy=True)
    product = db.relationship("Product", lazy=True)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default="created")  # created/cancelled/completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    buyer = db.relationship("User", lazy=True)

class OrderItem(db.Model):
    __tablename__ = "order_items"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    price_snapshot = db.Column(db.Numeric(10, 2), nullable=False)
    qty = db.Column(db.Integer, default=1, nullable=False)

    order = db.relationship("Order", lazy=True)
    product = db.relationship("Product", lazy=True)
