from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Article, db
from .forms import LoginForm, RegistrationForm, ArticleForm
from . import login_manager

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    articles = Article.query.all()
    return render_template("home.html", articles=articles)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='error')
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.home'))

@main.route("/sign-up", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', category='success')
        return redirect(url_for('main.login'))
    return render_template('sign-up.html', form=form)

@main.route("/article/new", methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(article)
        db.session.commit()
        flash('Your article has been created!', category='success')
        return redirect(url_for('main.home'))
    return render_template('create-posts.html', title='New Article', form=form, legend='New Article')

@main.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('posts.html', title=article.title, article=article)

@main.route("/article/<int:article_id>/update", methods=['GET', 'POST'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        flash('You do not have permission to edit this post.', category='error')
        return redirect(url_for('main.home'))
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash('Your article has been updated!', category='success')
        return redirect(url_for('main.article', article_id=article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.content.data = article.content
    return render_template('edit.html', title='Update Article', form=form, legend='Update Article')

@main.route("/article/<int:article_id>/delete", methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        flash('You do not have permission to delete this post.', category='error')
        return redirect(url_for('main.home'))
    db.session.delete(article)
    db.session.commit()
    flash('Your article has been deleted!', category='success')
    return redirect(url_for('main.home'))

@main.route("/about")
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Assuming there's a form and model to handle this, you'd process it here.
        flash("Message sent. We will get back to you shortly.", category='success')
        return redirect(url_for('main.home'))
    return render_template('contact.html')

