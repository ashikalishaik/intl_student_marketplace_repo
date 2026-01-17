from datetime import datetime
from ..extensions import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    condition = db.Column(db.String(50), default="Used")  # New/Used/Like New
    city = db.Column(db.String(120), default="")
    status = db.Column(db.String(20), default="pending")  # pending/approved/rejected/sold
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship("Category", lazy=True)
    media = db.relationship(
        "ProductMedia",
        backref="product",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="ProductMedia.sort_order"
    )


class ProductMedia(db.Model):
    __tablename__ = "product_media"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    media_type = db.Column(db.String(20), nullable=False)  # image / video
    url = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)