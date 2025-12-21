from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required
from ..extensions import db
from ..models import Product, Category
from ..forms import CategoryForm
from ..utils import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    pending = Product.query.filter_by(status="pending").order_by(Product.created_at.desc()).all()
    approved = Product.query.filter_by(status="approved").order_by(Product.created_at.desc()).limit(10).all()
    categories = Category.query.order_by(Category.type.asc(), Category.name.asc()).all()
    return render_template("admin/dashboard.html", pending=pending, approved=approved, categories=categories)

@admin_bp.route("/products/<int:product_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_product(product_id):
    p = Product.query.get_or_404(product_id)
    p.status = "approved"
    db.session.commit()
    flash("Product approved.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/products/<int:product_id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_product(product_id):
    p = Product.query.get_or_404(product_id)
    p.status = "rejected"
    db.session.commit()
    flash("Product rejected.", "warning")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/categories/new", methods=["GET","POST"])
@login_required
@admin_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data.strip()).first():
            flash("Category already exists.", "warning")
            return redirect(url_for("admin.new_category"))
        c = Category(name=form.name.data.strip(), type=form.type.data)
        db.session.add(c)
        db.session.commit()
        flash("Category added.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/new_category.html", form=form)
