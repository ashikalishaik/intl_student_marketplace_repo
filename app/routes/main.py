from flask import Blueprint, render_template, request
from ..models import Product, Category, Article
from ..extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    q = request.args.get("q", "").strip()
    city = request.args.get("city", "").strip()
    cat = request.args.get("cat", type=int)

    products_query = Product.query.filter(Product.status == "approved")
    if q:
        products_query = products_query.filter(Product.title.ilike(f"%{q}%"))
    if city:
        products_query = products_query.filter(Product.city.ilike(f"%{city}%"))
    if cat:
        products_query = products_query.filter(Product.category_id == cat)

    products = products_query.order_by(Product.created_at.desc()).limit(12).all()
    product_categories = Category.query.filter_by(type="product").order_by(Category.name.asc()).all()

    articles = Article.query.order_by(Article.updated_at.desc()).limit(5).all()
    return render_template("home.html", products=products, categories=product_categories, articles=articles)
