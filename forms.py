from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, Regexp
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.recaptcha import RecaptchaField

class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Отправить ссылку')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    privacy_consent = BooleanField('Я согласен на обработку персональных данных', validators=[DataRequired(message='Необходимо согласие на обработку персональных данных')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ResumeForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=18, max=70)])
    phone_number = StringField(
        'Телефон',
        validators=[
            DataRequired(),
            Regexp(r'^\+?\d{10,15}$', message="Введите корректный номер телефона (только цифры, возможно с + в начале)")
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    photo_file = FileField('Фото', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Только лицо')])
    description = TextAreaField('Описание', validators=[DataRequired()])
    privacy_consent = BooleanField('Я согласен на обработку персональных данных', validators=[DataRequired(message='Необходимо согласие на обработку персональных данных')])

    submit = SubmitField('Сохранить')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Новый пароль',
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Подтверждение пароля',
        validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')]
    )
    submit = SubmitField('Сбросить пароль')

from wtforms import IntegerField

class VacancyForm(FlaskForm):
    title = StringField('Название вакансии', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    experience = StringField('Требуемый опыт', validators=[DataRequired()])
    direction = StringField('Направление', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    salary_from = IntegerField('Зарплата от', validators=[Optional()])
    salary_to = IntegerField('Зарплата до', validators=[Optional()])
    submit = SubmitField('Добавить вакансию')