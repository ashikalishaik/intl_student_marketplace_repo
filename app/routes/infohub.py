from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Article, Category, Bookmark
from ..forms import ArticleForm
from ..utils import admin_required
from datetime import datetime

info_bp = Blueprint("info", __name__, url_prefix="/info")

@info_bp.route("/")
def info_home():
    q = request.args.get("q", "").strip()
    cat = request.args.get("cat", type=int)

    query = Article.query
    if q:
        query = query.filter(Article.title.ilike(f"%{q}%") | Article.tags.ilike(f"%{q}%"))
    if cat:
        query = query.filter(Article.category_id == cat)

    articles = query.order_by(Article.updated_at.desc()).all()
    categories = Category.query.filter_by(type="info").order_by(Category.name.asc()).all()
    return render_template("infohub/info_home.html", articles=articles, categories=categories)

@info_bp.route("/articles/<int:article_id>")
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    bookmarked = False
    if current_user.is_authenticated:
        bookmarked = Bookmark.query.filter_by(user_id=current_user.id, article_id=article_id).first() is not None
    return render_template("infohub/article_detail.html", article=article, bookmarked=bookmarked)

@info_bp.route("/bookmark/<int:article_id>", methods=["POST"])
@login_required
def toggle_bookmark(article_id):
    article = Article.query.get_or_404(article_id)
    bm = Bookmark.query.filter_by(user_id=current_user.id, article_id=article_id).first()
    if bm:
        db.session.delete(bm)
        db.session.commit()
        flash("Removed bookmark.", "info")
    else:
        bm = Bookmark(user_id=current_user.id, article_id=article_id)
        db.session.add(bm)
        db.session.commit()
        flash("Bookmarked!", "success")
    return redirect(url_for("info.article_detail", article_id=article_id))

@info_bp.route("/bookmarks")
@login_required
def my_bookmarks():
    bms = Bookmark.query.filter_by(user_id=current_user.id).all()
    articles = [bm.article for bm in bms]
    return render_template("infohub/bookmarks.html", articles=articles)

@info_bp.route("/admin/new", methods=["GET","POST"])
@admin_required
def admin_new_article():
    form = ArticleForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(type="info").order_by(Category.name.asc()).all()]
    if form.validate_on_submit():
        art = Article(
            category_id=form.category_id.data,
            author_id=current_user.id,
            title=form.title.data.strip(),
            content=form.content.data,
            tags=form.tags.data.strip(),
            updated_at=datetime.utcnow()
        )
        db.session.add(art)
        db.session.commit()
        flash("Article published.", "success")
        return redirect(url_for("info.article_detail", article_id=art.id))
    return render_template("infohub/admin_new_article.html", form=form)
