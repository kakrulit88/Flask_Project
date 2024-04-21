from flask import Flask, request, make_response, render_template, redirect, abort
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField, \
    FloatField, DateTimeField, DateField
from wtforms.validators import DataRequired
from datetime import date


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    age = IntegerField('Ваш возраст')
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироватся')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class LoanForm(FlaskForm):
    value = IntegerField('Cумма займa/кредита', validators=[DataRequired()], default=100000)
    percent = FloatField('Процентная ставка/ % годовых', validators=[DataRequired()], default=5.00)
    currency = SelectField('Валюта',
                           choices=[('₽', '₽'), ('$', '$'), ('€', '€'), ('¥', '¥')],
                           validate_choice=False, validators=[DataRequired()])
    loan_time = IntegerField('Срок кредита/займа', validators=[DataRequired()], default=3)
    loan_time_type = SelectField(
        choices=[('года', 'года'), ('месяца', 'месяца')],
        validate_choice=False, validators=[DataRequired()])

    loan_date = DateField('Дата выдачи', validators=[DataRequired()], default=date.today())
    pay_type = SelectField('Порядок погашения',
                           choices=[('Аннуитетный', 'Аннуитетный'), ('Дифференцированный', 'Дифференцированный')],
                           validate_choice=False, validators=[DataRequired()])
    submit = SubmitField('Расчитать')


class DepositForm(FlaskForm):
    value = IntegerField('Cумма вклада', validators=[DataRequired()], default=1000000)
    currency = SelectField('Валюта',
                           choices=[('₽', '₽'), ('$', '$'), ('€', '€'), ('¥', '¥')],
                           validate_choice=False, validators=[DataRequired()])
    deposit_time = IntegerField('Срок вклада', validators=[DataRequired()], default=1)
    deposit_time_type = SelectField(
        choices=[('года', 'года'), ('месяца', 'месяца')],
        validate_choice=False, validators=[DataRequired()])
    percent = FloatField('Процентная ставка/ % годовых', validators=[DataRequired()], default=5.00)
    loan_date = DateField('Дата открытия', validators=[DataRequired()], default=date.today())
    submit = SubmitField('Расчитать')