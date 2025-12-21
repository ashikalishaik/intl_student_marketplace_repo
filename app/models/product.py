from datetime import datetime
from ..extensions import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    condition = db.Column(db.String(50), default="Used")  # New/Used/Like New
    city = db.Column(db.String(120), default="")
    status = db.Column(db.String(20), default="pending")  # pending/approved/rejected/sold
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship("Category", lazy=True)
    images = db.relationship("ProductImage", backref="product", cascade="all, delete-orphan", lazy=True)

class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
