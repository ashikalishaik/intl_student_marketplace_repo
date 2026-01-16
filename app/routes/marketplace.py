from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Product, Category, ProductImage, Cart, CartItem, Order, OrderItem, Conversation, Message
from ..forms import ProductForm, MessageForm
from ..utils import admin_required

market_bp = Blueprint("market", __name__, url_prefix="/market")

@market_bp.route("/products")
def products():
    q = request.args.get("q", "").strip()
    city = request.args.get("city", "").strip()
    cat = request.args.get("cat", type=int)

    query = Product.query.filter(Product.status == "approved")
    if q:
        query = query.filter(Product.title.ilike(f"%{q}%"))
    if city:
        query = query.filter(Product.city.ilike(f"%{city}%"))
    if cat:
        query = query.filter(Product.category_id == cat)

    products = query.order_by(Product.created_at.desc()).all()
    categories = Category.query.filter_by(type="product").order_by(Category.name.asc()).all()
    return render_template("marketplace/products.html", products=products, categories=categories)

@market_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if product.status != "approved" and (not current_user.is_authenticated or (not current_user.is_admin() and product.seller_id != current_user.id)):
        abort(404)
    return render_template("marketplace/product_detail.html", product=product)

@market_bp.route("/sell", methods=["GET","POST"])
@login_required
def sell():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(type="product").order_by(Category.name.asc()).all()]

    if form.validate_on_submit():
        product = Product(
            seller_id=current_user.id,
            category_id=form.category_id.data,
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            price=form.price.data,
            condition=form.condition.data,
            city=(form.city.data.strip() or current_user.city),
            status="pending"
        )
        db.session.add(product)
        db.session.commit()

        if form.image_url.data.strip():
            img = ProductImage(product_id=product.id, image_url=form.image_url.data.strip())
            db.session.add(img)
            db.session.commit()

        flash("Listing submitted for review. It will appear after admin approval.", "success")
        return redirect(url_for("market.my_listings"))

    return render_template("marketplace/sell.html", form=form)

@market_bp.route("/my-listings")
@login_required
def my_listings():
    products = Product.query.filter_by(seller_id=current_user.id).order_by(Product.created_at.desc()).all()
    return render_template("marketplace/my_listings.html", products=products)

@market_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_listing(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id and not current_user.is_admin():
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash("Listing deleted.", "info")
    return redirect(url_for("market.my_listings"))

# CART
@market_bp.route("/cart")
@login_required
def cart_view():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
    total = sum(Decimal(str(it.product.price)) * it.qty for it in items)
    return render_template("marketplace/cart.html", items=items, total=total)

@market_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def cart_add(product_id):
    product = Product.query.get_or_404(product_id)
    if product.status != "approved":
        abort(404)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.qty += 1
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, qty=1)
        db.session.add(item)
    db.session.commit()
    flash("Added to cart.", "success")
    return redirect(url_for("market.cart_view"))

@market_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
@login_required
def cart_remove(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        return redirect(url_for("market.cart_view"))
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Removed from cart.", "info")
    return redirect(url_for("market.cart_view"))

@market_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        flash("Cart is empty.", "warning")
        return redirect(url_for("market.cart_view"))
    items = CartItem.query.filter_by(cart_id=cart.id).all()
    if not items:
        flash("Cart is empty.", "warning")
        return redirect(url_for("market.cart_view"))

    # Create order
    total = sum(Decimal(str(it.product.price)) * it.qty for it in items)
    order = Order(buyer_id=current_user.id, total=total, status="created")
    db.session.add(order)
    db.session.commit()

    for it in items:
        oi = OrderItem(order_id=order.id, product_id=it.product_id, price_snapshot=it.product.price, qty=it.qty)
        db.session.add(oi)
    # clear cart
    for it in items:
        db.session.delete(it)
    db.session.commit()

    flash(f"Order #{order.id} created (demo checkout).", "success")
    return redirect(url_for("market.orders"))

@market_bp.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("marketplace/orders.html", orders=orders)

# Messaging (basic)
@market_bp.route("/contact-seller/<int:product_id>", methods=["GET","POST"])
@login_required
def contact_seller(product_id):
    product = Product.query.get_or_404(product_id)
    if product.status != "approved":
        abort(404)
    if product.seller_id == current_user.id:
        flash("You are the seller of this item.", "warning")
        return redirect(url_for("market.product_detail", product_id=product_id))

    conv = Conversation.query.filter_by(buyer_id=current_user.id, seller_id=product.seller_id, product_id=product_id).first()
    if not conv:
        conv = Conversation(buyer_id=current_user.id, seller_id=product.seller_id, product_id=product_id)
        db.session.add(conv)
        db.session.commit()

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(conversation_id=conv.id, sender_id=current_user.id, text=form.text.data.strip())
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for("market.contact_seller", product_id=product_id))

    messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.created_at.asc()).all()
    return render_template("marketplace/contact_seller.html", product=product, form=form, messages=messages)

@market_bp.route("/inbox")
@login_required
def inbox():
    # show conversations where user is buyer or seller
    convs = Conversation.query.filter(
        (Conversation.buyer_id == current_user.id) | (Conversation.seller_id == current_user.id)
    ).order_by(Conversation.created_at.desc()).all()
    products = {c.product_id: Product.query.get(c.product_id) for c in convs}
    return render_template("marketplace/inbox.html", convs=convs, products=products)

@market_bp.route("/conversations/<int:conversation_id>", methods=["GET", "POST"])
@login_required
def conversation_detail(conversation_id):
    convo = Conversation.query.get_or_404(conversation_id)

    # allow only buyer or seller to view
    if current_user.id not in (convo.buyer_id, convo.seller_id):
        abort(403)

    product = Product.query.get(convo.product_id)

    if request.method == "POST":
        text = (request.form.get("message") or "").strip()
        if not text:
            flash("Message cannot be empty.", "warning")
            return redirect(url_for("market.conversation_detail", conversation_id=convo.id))

        msg = Message(
            conversation_id=convo.id,
            sender_id=current_user.id,
            text=text  # IMPORTANT: change to your actual column name if not 'content'
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for("market.conversation_detail", conversation_id=convo.id))

    # IMPORTANT: do NOT filter by sender_id
    messages = (Message.query
                .filter_by(conversation_id=convo.id)
                .order_by(Message.created_at.asc() if hasattr(Message, "created_at") else Message.id.asc())
                .all())

    return render_template(
        "marketplace/conversation_detail.html",
        convo=convo,
        product=product,
        messages=messages
    )


