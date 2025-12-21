from ..extensions import db

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False)  # product | info

    def __repr__(self):
        return f"<Category {self.type}:{self.name}>"
