from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Article, db
from .forms import LoginForm, RegistrationForm, ArticleForm
from . import login_manager

main = Blueprint('main', __name__)

@main.route("/")
@main.route('/home')
def home():
    articles = Article.query.all()
    user = current_user  # или другой способ получения данных пользователя
    return render_template("home.html", articles=articles, user=user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email= request.form.get("email")
        password = request.form.get("password1")


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.home'))

@main.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("passsword2")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("This username already exists.")
            return redirect(url_for('sign_up'))

        email_exists =User.query.filter_by(email=email).first()
        if email_exists:
            flash("This email is already registered.")
            return redirect(url_for('sign_up'))

        password = generate_password_hash(password1)
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('User created')
        return redirect(url_for('main.home'))

    return render_template('sign-up.html', user=current_user)

@main.route("/create-posts", methods = ['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')


        if not text:
            flash('field can not be empty', category='error')
        else:
            article = Article(text=text, author=current_user.id)
            db.session.add(article)
            db.session.commit()
            flash('Article created successfully', category='success')
            return redirect(url_for('main.home'))
    return render_template('create_posts.html', user=current_user)

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

@main.route("/delete-post/<id>", methods=['GET'])
@login_required
def delete_post(id):
    article = Article.query.filter_by(id=id).first()

    if not article:
        flash("Post does not exist.", category='error')
    elif current_user.id != article.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(article)
        db.session.commit()
        flash('Article deleted.', category='success')

    return redirect(url_for('main.home'))

@main.route('/search', methods=['POST'])
def search():
    search_word = request.form['search']
    results = Article.query.filter(Article.text.like(f'%{search_word}%')).all()
    return render_template('search_results.html', posts=results)



