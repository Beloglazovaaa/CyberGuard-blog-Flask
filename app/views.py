from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Article, db

from . import login_manager
from flask_login import current_user
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import joblib

import keras
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.models import *
from tensorflow.keras.layers import Dense

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

@main.route('/train_model_polynomial', methods=['POST'])
def train_model_polynomial():
    data = pd.read_csv('myblog/diabetes.csv')

    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    # Масштабирование признаков
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)

    # Создание и обучение модели логистической регрессии
    model = LogisticRegression()
    model.fit(X_scaled, y)

    # Сохранение обученной модели для последующего использования
    joblib.dump(model, 'polynomial_regression_model.pkl')
    return model, scaler
    return "Модель обучена и сохранена."

from .models import DiabetesModel
from flask import request, jsonify
from sklearn.externals import joblib

@main.route('/predict_diabetes_polynomial', methods=['POST'])
def predict_diabetes_polynomial(request):
    # Получение данных из POST-запроса
    pregnancies = float(request.POST.get('pregnancies'))
    glucose = float(request.POST['glucose'])
    blood_pressure = float(request.POST.get('blood-pressure'))
    skin_thickness = float(request.POST.get('skin-thickness'))
    insulin = float(request.POST.get('insulin'))
    bmi = float(request.POST.get('bmi'))
    diabetes_pedigree_function = float(request.POST.get('diabetes-pedigree'))
    age = float(request.POST.get('age'))

    model, scaler = train_model_polynomial()

    model = joblib.load('polynomial_regression_model.pkl')
    # Масштабирование введенных пользователем данных
    user_data = scaler.transform(
        [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])

    # Предсказание вероятности возникновения диабета
    probability = model.predict_proba(user_data)[:, 1][0]

    # Сохранение предсказанных данных в базе данных
    DiabetesModel.objects.create(pregnancies=pregnancies, glucose=glucose, bloodpressure=blood_pressure,
                                 skinthickness=skin_thickness, insulin=insulin, bmi=bmi,
                                 diabetespedigreefunction=diabetes_pedigree_function, age=age,
                                 probability=probability)

    # Возврат предсказанной вероятности диабета в формате JSON
    return jsonify({'probability': probability})


def train_model_gradient():
    data = pd.read_csv('myblog/diabetes.csv')

    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    # Масштабирование признаков
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)

    # Создание и обучение модели логистической регрессии
    model = GradientBoostingClassifier()
    model.fit(X_scaled, y)

    # Сохранение обученной модели для последующего использования
    joblib.dump(model, 'gradient_boosting_model.pkl')
    return model, scaler
    return "Модель обучена и сохранена."


def predict_diabetes_gradient(request):
    # Получение данных из POST-запроса
    pregnancies = float(request.POST.get('pregnancies'))
    glucose = float(request.POST['glucose'])
    blood_pressure = float(request.POST.get('blood-pressure'))
    skin_thickness = float(request.POST.get('skin-thickness'))
    insulin = float(request.POST.get('insulin'))
    bmi = float(request.POST.get('bmi'))
    diabetes_pedigree_function = float(request.POST.get('diabetes-pedigree'))
    age = float(request.POST.get('age'))

    model, scaler = train_model_gradient()

    model = joblib.load('gradient_boosting_model.pkl')
    # Масштабирование введенных пользователем данных
    user_data = scaler.transform(
        [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])

    # Предсказание вероятности возникновения диабета
    probability = model.predict_proba(user_data)[:, 1][0]

    # Сохранение предсказанных данных в базе данных
    DiabetesModel.objects.create(pregnancies=pregnancies, glucose=glucose, bloodpressure=blood_pressure,
                                 skinthickness=skin_thickness, insulin=insulin, bmi=bmi,
                                 diabetespedigreefunction=diabetes_pedigree_function, age=age,
                                 probability=probability)

    # Возврат предсказанной вероятности диабета в формате JSON
    return jsonify({'probability': probability})

def build_model(input_shape):
    model = keras.Sequential([
        SimpleRNN(50, return_sequences=True, input_shape=input_shape),
        SimpleRNN(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from keras.layers import SimpleRNN, Dense

model = None
scaler = None


def build_model(input_shape):
    model = keras.Sequential([
        SimpleRNN(50, return_sequences=True, input_shape=input_shape),
        SimpleRNN(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_model_recurrent():
    # Загрузка данных
    data = pd.read_csv('myblog/diabetes.csv')

    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    # Масштабирование признаков
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = build_model((X_scaled.shape[1], 1))
    model.fit(X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1)), y, epochs=10, batch_size=32)
    model.save_weights('rnn_model.weights.h5')

    return model, scaler


def predict_diabetes_recurrent(request):
    pregnancies = float(request.POST.get('pregnancies'))
    glucose = float(request.POST['glucose'])
    blood_pressure = float(request.POST.get('blood-pressure'))
    skin_thickness = float(request.POST.get('skin-thickness'))
    insulin = float(request.POST.get('insulin'))
    bmi = float(request.POST.get('bmi'))
    diabetes_pedigree_function = float(request.POST.get('diabetes-pedigree'))
    age = float(request.POST.get('age'))

    global model, scaler
    if request.method == 'POST':
        if model is None:
            model, scaler = train_model_recurrent()
        else:
            model.load_weights('rnn_model.weights.h5')

        # Load scaler object
        if scaler is None:
            scaler = StandardScaler()  # Assuming you saved the scaler object separately

        # Get input data from POST request
        input_data = {
            'pregnancies': float(request.POST.get('pregnancies')),
            'glucose': float(request.POST.get('glucose')),
            'blood_pressure': float(request.POST.get('blood-pressure')),
            'skin_thickness': float(request.POST.get('skin-thickness')),
            'insulin': float(request.POST.get('insulin')),
            'bmi': float(request.POST.get('bmi')),
            'diabetes_pedigree': float(request.POST.get('diabetes-pedigree')),
            'age': float(request.POST.get('age'))
        }

        # Масштабирование входных данных пользователя
        scaled_input = scaler.transform([list(input_data.values())])

        # Изменение формы входных данных для модели RNN
        reshaped_input = scaled_input.reshape((1, scaled_input.shape[1], 1))

        # Предсказание вероятности диабета
        probability = float(model.predict(reshaped_input)[0])

        # Сохранение предсказанных данных в базу данных
        DiabetesModel.objects.create(pregnancies=pregnancies, glucose=glucose, bloodpressure=blood_pressure,
                                     skinthickness=skin_thickness, insulin=insulin, bmi=bmi,
                                     diabetespedigreefunction=diabetes_pedigree_function, age=age,
                                     probability=probability)
        # Возврат предсказанной вероятности диабета в формате JSON-ответа
        return jsonify({'probability': probability})
    else:
        return jsonify({'error': 'Invalid request method'})

def get_latest_diabetes_prediction(request):
    if request.method == 'GET':
        # Получаем последнюю запись из таблицы DiabetesModel
        latest_prediction = DiabetesModel.objects.latest('id')

        # Формируем JSON-ответ с последним результатом
        response_data = {
            'probability': latest_prediction.probability
        }

        # Возвращаем JSON-ответ
        return jsonify(response_data)
