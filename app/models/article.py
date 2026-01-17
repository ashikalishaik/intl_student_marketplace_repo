from datetime import datetime
from ..extensions import db

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(250), default="")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship("Category", lazy=True)

class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", lazy=True)
    article = db.relationship("Article", lazy=True)
