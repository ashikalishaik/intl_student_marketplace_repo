from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required
from ..extensions import db
from ..models import Product, Category, Article
from ..forms import CategoryForm, AdminProductEditForm
from ..utils import admin_required
from datetime import datetime

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

@admin_bp.route("/products")
@login_required
@admin_required
def products_list():
    show = request.args.get("show", "active")  # active | deleted | all
    q = Product.query

    if show == "active":
        q = q.filter(Product.is_deleted == False)
    elif show == "deleted":
        q = q.filter(Product.is_deleted == True)

    products = q.order_by(Product.created_at.desc()).all()
    return render_template("admin/products_list.html", products=products, show=show)


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    form = AdminProductEditForm(obj=p)
    form.category_id.choices = [(c.id, f"{c.type} / {c.name}") for c in Category.query.order_by(Category.type.asc(), Category.name.asc()).all()]

    if form.validate_on_submit():
        p.title = form.title.data.strip()
        p.description = form.description.data
        p.price = form.price.data
        p.condition = form.condition.data
        p.city = form.city.data.strip()
        p.category_id = form.category_id.data
        p.status = form.status.data
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.products_list"))

    return render_template("admin/edit_product.html", form=form, product=p)


@admin_bp.route("/products/<int:product_id>/soft-delete", methods=["POST"])
@login_required
@admin_required
def soft_delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    p.is_deleted = True
    p.deleted_at = datetime.utcnow()
    db.session.commit()
    flash("Product soft-deleted.", "warning")
    return redirect(url_for("admin.products_list"))


@admin_bp.route("/products/<int:product_id>/restore", methods=["POST"])
@login_required
@admin_required
def restore_product(product_id):
    p = Product.query.get_or_404(product_id)
    p.is_deleted = False
    p.deleted_at = None
    db.session.commit()
    flash("Product restored.", "success")
    return redirect(url_for("admin.products_list", show="deleted"))


@admin_bp.route("/products/<int:product_id>/hard-delete", methods=["POST"])
@login_required
@admin_required
def hard_delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash("Product permanently deleted.", "danger")
    return redirect(url_for("admin.products_list", show="deleted"))

