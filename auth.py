from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models import User, PasswordResetToken, Resume
from forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm
from extensions import db
from utils import send_email, log_security_event
from flask_wtf.csrf import generate_csrf
from urllib.parse import urlparse
from extensions import limiter

auth_bp = Blueprint('auth', __name__)

# ВНИМАНИЕ: serializer теперь создается ВНУТРИ функций, с использованием current_app
# потому что глобально app в этом модуле недоступен.

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html', form=form)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='candidate'
        )
        new_user.password = form.password.data
        # Генерируем токен подтверждения email
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(new_user.email, salt='email-confirm')
        new_user.email_confirm_token = token
        db.session.add(new_user)
        db.session.commit()
        # Отправляем письмо с подтверждением
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        body = f"""
Здравствуйте!

Для подтверждения регистрации на сайте Road Fighters перейдите по ссылке:
{confirm_url}

Если вы не регистрировались, просто проигнорируйте это письмо.
"""
        send_email('Подтверждение регистрации', [new_user.email], body)
        flash('На вашу почту отправлено письмо для подтверждения регистрации.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash('Срок действия ссылки истёк. Запросите регистрацию заново.', 'danger')
        return redirect(url_for('auth.register'))
    except BadSignature:
        flash('Некорректная ссылка подтверждения.', 'danger')
        return redirect(url_for('auth.register'))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('auth.register'))
    if user.email_confirmed:
        flash('Email уже подтверждён.', 'info')
        return redirect(url_for('auth.login'))
    user.email_confirmed = True
    user.email_confirm_token = None
    db.session.commit()
    flash('Email успешно подтверждён! Теперь вы можете войти.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per 10 minutes')
def login():
    if current_user.is_authenticated:
        # Если профиль не заполнен — редиректим на setup
        if not (current_user.role and current_user.city and current_user.license_category and current_user.citizenship):
            return redirect(url_for('routes.profile_setup'))
        # Если профиль заполнен — редиректим по роли
        if current_user.role == 'candidate':
            return redirect(url_for('routes.profile_candidate'))
        elif current_user.role == 'employer':
            return redirect(url_for('routes.profile_employer'))
        else:
            return redirect(url_for('routes.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=False)
            # После входа — проверяем профиль
            if not (user.role and user.city and user.license_category and user.citizenship):
                return redirect(url_for('routes.profile_setup'))
            if user.role == 'candidate':
                return redirect(url_for('routes.profile_candidate'))
            elif user.role == 'employer':
                return redirect(url_for('routes.profile_employer'))
            else:
                return redirect(url_for('routes.index'))
        else:
            log_security_event('Неудачная попытка входа', f"email={form.email.data}, ip={request.remote_addr}")
            flash('Неправильный email или пароль', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/profile')
@login_required
def profile():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, resumes=resumes)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('routes.index'))

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
@limiter.limit('5 per 10 minutes')
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = ResetRequestForm()
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password_token', token=token, _external=True)
            prt = PasswordResetToken(user_id=user.id, token=token)
            db.session.add(prt)
            db.session.commit()
            body = f"Перейдите по ссылке для сброса пароля:\n{reset_url}\nСсылка действует 30 минут."
            send_email("Сброс пароля", [email], body)
            flash('Ссылка для сброса пароля отправлена на почту', 'info')
        else:
            log_security_event('Неудачная попытка сброса пароля', f"email={email}, ip={request.remote_addr}")
            flash('Пользователь с таким email не найден', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='password-reset-salt', max_age=1800)
    except Exception:
        flash('Ссылка для сброса пароля недействительна или устарела', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if password and password == confirm:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Пароль успешно сброшен. Войдите с новым паролем.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Пароли не совпадают', 'danger')

    return render_template('reset_password.html',form=form)
