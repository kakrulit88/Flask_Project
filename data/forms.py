from flask import Flask, request, make_response, render_template, redirect, abort
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired


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
    value = StringField(validators=[DataRequired()])
    percent = FloatField('Процентная ставка')
    currency = SelectField('валюта',
                                choices=[('$', '$'), ('€', '€'), ('¥', '¥')],
                                validate_choice=False, validators=[DataRequired()])
    submit = SubmitField('asd')