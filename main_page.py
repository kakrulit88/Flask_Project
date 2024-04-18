from datetime import timedelta

from flask import Flask, request, make_response, render_template, redirect, abort, url_for

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import requests
from bs4 import BeautifulSoup
import lxml

from data.users import User
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


def get_annuity_loan_table(value, percent, loan_time, loan_time_type, loan_date):
    monthly_percent = percent / 1200
    if loan_time_type == 'года':
        loan_time *= 12

    monthly_payment = round(value * (
            monthly_percent * ((1 + monthly_percent) ** loan_time) / ((1 + monthly_percent) ** loan_time - 1)), 2)

    month_count = (loan_date + timedelta(weeks=loan_time * 4))
    total_loan_cost = 0
    all_payments = value
    loan_table = {'total_loan_cost': 0,
                  'all_payments': 0,
                  'table': [{'id': 0,
                             'payment date': str(loan_date),
                             'monthly_payment': "{0:0.2f}".format(0.00),
                             'overpay_loan': "{0:0.2f}".format(0.00),
                             'overpay_per': "{0:0.2f}".format(0.00),
                             'left': value}]
                  }
    for month in range(1, loan_time + 1):
        loan_date += timedelta(days=30)
        overpay_per = round(value * monthly_percent, 2)
        overpay_loan = round(monthly_payment - overpay_per, 2)
        value = round(value + overpay_per - monthly_payment, 2)
        total_loan_cost += overpay_per
        loan_table['table'].append({'id': month,
                                    'payment date': str(loan_date),
                                    'monthly_payment': monthly_payment,
                                    'overpay_loan': overpay_loan,
                                    'overpay_per': "{0:0.2f}".format(overpay_per),
                                    'left': "{0:0.2f}".format(value)})

    total_loan_cost = round(total_loan_cost)
    all_payments += total_loan_cost
    loan_table['total_loan_cost'] = total_loan_cost
    loan_table['all_payments'] = all_payments
    loan_table['table'][-1]['left'] = 0

    return loan_table


def get_different_loan_table(value, percent, loan_time, loan_time_type, loan_date):
    if loan_time_type == 'года':
        loan_time *= 12
    monthly_payment_without_pers = round(value / loan_time, 2)

    total_loan_cost = 0
    all_payments = value
    loan_table = {'total_loan_cost': 0,
                  'all_payments': 0,
                  'table': [{'id': 0,
                             'payment date': str(loan_date),
                             'monthly_payment': "{0:0.2f}".format(0.00),
                             'overpay_loan': "{0:0.2f}".format(0.00),
                             'overpay_per': "{0:0.2f}".format(0.00),
                             'left': value}]
                  }

    for month in range(1, loan_time + 1):
        loan_date += timedelta(days=30)
        monthly_pers = round((value * (percent / 100) * 30) / 365, 2)
        monthly_payment = round(monthly_payment_without_pers + monthly_pers, 2)
        total_loan_cost += monthly_pers
        value -= monthly_payment_without_pers
        loan_table['table'].append({'id': month,
                                    'payment date': str(loan_date),
                                    'monthly_payment': "{0:0.2f}".format(monthly_payment),
                                    'overpay_loan': monthly_payment_without_pers,
                                    'overpay_per': "{0:0.2f}".format(monthly_pers),
                                    'left': "{0:0.2f}".format(value)})

    total_loan_cost = round(total_loan_cost)
    all_payments += total_loan_cost
    loan_table['total_loan_cost'] = total_loan_cost
    loan_table['all_payments'] = all_payments
    loan_table['table'][-1]['left'] = 0

    return loan_table


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

        return render_template('loan_table.html', loan_table=loan_table, currency=currency)
    return render_template('calc_loan.html', title='Кредитный калькулятор', form=form)


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


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.hashed_password, password)


if __name__ == '__main__':
    db_session.global_init('db/users_data.db')
    app.run(port=8080, host='127.0.0.1')
