from flask import Flask, request, make_response, render_template, redirect, abort, url_for
from flask_restful import reqparse, abort, Api, Resource
from data.api_resources import DepositApi, LoanApi
import os

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from data.users import User
from data import db_session
from data.forms import *
from data.calculators import get_annuity_loan_table, get_different_loan_table, get_deposit_table

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
MAIN_URL = 'https://sasha31q.pythonanywhere.com/'

api = Api(app)
api.add_resource(LoanApi, '/api/calc_loan')
api.add_resource(DepositApi, '/api/calc_deposit')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Финансовые калькуляторы')


@app.route('/calc/loan', methods=['POST', 'GET'])
def calc_loan():
    form = LoanForm()
    if request.method == 'POST':
        value = form.value.data
        percent = form.percent.data
        loan_time = form.loan_time.data
        loan_time_type = form.loan_time_type.data
        loan_date = form.loan_date.data
        pay_type = form.pay_type.data
        currency = form.currency.data
        if pay_type == 'Аннуитетный':
            loan_table = get_annuity_loan_table(value=value, percent=percent, loan_time=loan_time,
                                                loan_time_type=loan_time_type,
                                                loan_date=loan_date)
        else:
            loan_table = get_different_loan_table(value=value, percent=percent, loan_time=loan_time,
                                                  loan_time_type=loan_time_type,
                                                  loan_date=loan_date)

        return render_template('loan_table.html', title='Кредитный калькулятор', loan_table=loan_table,
                               currency=currency)
    return render_template('calc_loan.html', title='Кредитный калькулятор', form=form)


@app.route('/calc/deposit', methods=['POST', 'GET'])
def calc_deposit():
    form = DepositForm()
    if request.method == 'POST':
        value = form.value.data
        currency = form.currency.data
        percent = form.percent.data
        deposit_time = form.deposit_time.data
        deposit_time_type = form.deposit_time_type.data
        deposit_date = form.loan_date.data
        deposit_table = get_deposit_table(value, percent, deposit_time, deposit_time_type, deposit_date)
        return render_template('deposit_table.html', title='Депозитный калькулятор', deposit_table=deposit_table,
                               currency=currency)
    return render_template('calc_deposit.html', title='Депозитный калькулятор', form=form)


@app.route('/api_info')
def api():
    return render_template('api_info.html', title='Апи: кредиты/вклады', MAIN_URL=MAIN_URL)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Авторизация', form=form, message='Неверный логин или пароль')
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
    return redirect('/')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/register')


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.hashed_password, password)


if __name__ == '__main__':
    db_session.global_init('db/users_data.db')
    app.run(port=8080, host='127.0.0.1')
