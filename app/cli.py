from flask import current_app
from .extensions import db
from .models import User, Category, Cart

def register_cli(app):
    @app.cli.command("create-admin")
    def create_admin():
        """Create an admin user. Prompts in terminal."""
        import getpass
        name = input("Admin name: ").strip()
        email = input("Admin email: ").strip().lower()
        password = getpass.getpass("Admin password: ")

        if User.query.filter_by(email=email).first():
            print("User already exists.")
            return

        user = User(name=name, email=email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

        print("Admin created.")

    @app.cli.command("seed")
    def seed():
        """Seed starter categories and sample articles/products (safe for dev)."""
        from .models import Article, Product, ProductImage
        from datetime import datetime
        import random
        from decimal import Decimal

        # categories
        product_cats = ["Furniture", "Electronics", "Books", "Winter Gear", "Kitchen", "Housing"]
        info_cats = ["Immigration", "Jobs", "Housing", "Banking", "Healthcare", "Driving", "Taxes"]

        for n in product_cats:
            if not Category.query.filter_by(name=n).first():
                db.session.add(Category(name=n, type="product"))
        for n in info_cats:
            if not Category.query.filter_by(name=n).first():
                db.session.add(Category(name=n, type="info"))
        db.session.commit()

        admin = User.query.filter_by(role="admin").first()
        if not admin:
            print("No admin user found. Run: flask create-admin")
            return

        # sample articles
        samples = [
            ("F-1 Essentials: What to do in your first 7 days",
             "Start with housing + bank account + campus check-in. Keep copies of your passport, visa, I-20, and I-94. Learn your DSO contact info.\n\nThis is a starter article — edit in Admin > New Article.",
             "f1,i20,i94,arrival"),
            ("SSN Basics for International Students",
             "SSN is usually for on-campus employment. Ask your DSO about eligibility and required letters.\n\nStarter content — update with your local steps.",
             "ssn,on-campus,documents"),
            ("How to Buy Used Items Safely",
             "Meet in public places, verify product condition, and avoid sending money to unknown accounts.\n\nStarter content — update with your local marketplace rules.",
             "safety,marketplace,scams"),
        ]
        info_category = Category.query.filter_by(type="info").first()
        for title, content, tags in samples:
            if not Article.query.filter_by(title=title).first():
                db.session.add(Article(
                    category_id=info_category.id,
                    author_id=admin.id,
                    title=title,
                    content=content,
                    tags=tags,
                    updated_at=datetime.utcnow()
                ))
        db.session.commit()

        # sample products
        seller = User.query.filter_by(role="admin").first()
        prod_cat = Category.query.filter_by(type="product").first()
        if prod_cat and seller:
            for i in range(4):
                title = f"Starter Listing #{i+1} - Desk Lamp"
                if not Product.query.filter_by(title=title).first():
                    p = Product(
                        seller_id=seller.id,
                        category_id=prod_cat.id,
                        title=title,
                        description="Sample listing. Replace with real items.",
                        price=Decimal("15.00") + i,
                        condition="Used",
                        city="Fairfax",
                        status="approved"
                    )
                    db.session.add(p)
                    db.session.commit()
                    db.session.add(ProductImage(product_id=p.id, image_url="https://picsum.photos/seed/lamp/800/600"))
                    db.session.commit()

        print("Seed complete.")
