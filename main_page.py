from flask import Flask, request, make_response, render_template, redirect, abort
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup
import lxml

from data.users import User

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def get_value():
    url = 'https://www.google.com/search?q=курс+рубля+к+валютам'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    result = soup.find("div", class_="webanswers-webanswers_table__webanswers-table").find('table').find_all('th')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Финансовые калькуляторы')


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.email = form.email.data
        if form.password_again.data == form.password.data:
            user.hashed_password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init('db/users_data.db')
    app.run(port=8080, host='127.0.0.1')
