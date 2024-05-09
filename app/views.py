from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Article, db
from .forms import LoginForm, RegistrationForm, ArticleForm
from . import login_manager
from flask_login import current_user


main = Blueprint('main', __name__)

@main.route("/")
@main.route('/home')

def home():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.paginate(page=page, per_page=3, error_out=False)
    articles = pagination.items
    return render_template("home.html", articles=articles, user=current_user, pagination=pagination)

@main.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Article.query.get_or_404(post_id)  # Получаем объект Article по его идентификатору
    return render_template('post_detail.html', post=post)


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

@main.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Проверка на пустые поля
        if not (username and first_name and last_name and email and password1 and password2):
            flash("Пожалуйста, заполните все поля.")
            return redirect(url_for('main.sign_up'))

        # Проверка на совпадение паролей
        if password1 != password2:
            flash("Пароли не совпадают.")
            return redirect(url_for('main.sign_up'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Это имя пользователя уже занято.")
            return redirect(url_for('main.sign_up'))

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Этот адрес электронной почты уже зарегистрирован.")
            return redirect(url_for('main.sign_up'))

        password = generate_password_hash(password1)
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Пользователь создан.')
        return redirect(url_for('main.home'))

    return render_template('sign-up.html', user=current_user)


@main.route("/create-posts", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if not title or not text:
            flash('Title and text fields cannot be empty', category='error')
        else:
            article = Article(title=title, text=text, author=current_user.id)
            db.session.add(article)
            db.session.commit()
            flash('Article created successfully', category='success')
            return redirect(url_for('main.home'))
    return render_template('create_posts.html', user=current_user)


@main.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('posts.html', title=article.title, article=article)



@main.route('/polynomial_regression')
def polynomial_regression():
    return render_template('polynomial_regression.html')

@main.route('/gradient_boosting')
def gradient_boosting():
    return render_template('gradient_boosting.html')

@main.route('/recurrent_neural_network')
def recurrent_neural_network():
    return render_template('recurrent_neural_network.html')


