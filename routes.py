from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app, send_from_directory, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
from flask_wtf.csrf import generate_csrf
from models import User, Vacancy, Resume, ResponseVacancy, PasswordResetToken, City
from forms import ResumeForm, VacancyForm, LoginForm, RegistrationForm
from extensions import db
from utils import notify_new_response
from decorators import owner_required
from math import ceil
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from oauth import oauth, handle_oauth_callback
from PIL import Image
from io import BytesIO

routes_bp = Blueprint('routes', __name__)

# Обработчик ошибки для AnonymousUserMixin
@routes_bp.app_errorhandler(AttributeError)
def handle_attribute_error(e):
    if "'AnonymousUserMixin' object has no attribute 'id'" in str(e):
        flash('Для доступа к этой странице необходимо войти в систему', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('500.html'), 500

@routes_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@routes_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@routes_bp.app_errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@routes_bp.route('/')
def index():
    vacancies = Vacancy.query.order_by(Vacancy.created_at.desc()).all()
    return render_template('index.html', vacancies=vacancies)

@routes_bp.route('/privacy-policy')
def privacy_policy():
    """Страница политики конфиденциальности"""
    return render_template('privacy_policy.html')

# OAuth маршруты
@routes_bp.route('/auth/vk')
def vk_login():
    """Авторизация через ВКонтакте"""
    redirect_uri = url_for('routes.vk_callback', _external=True)
    return oauth.vk.authorize_redirect(redirect_uri)

@routes_bp.route('/auth/vk/callback')
def vk_callback():
    """Callback для ВКонтакте"""
    user = handle_oauth_callback('vk')
    if user:
        flash(f'Добро пожаловать, {user.username}!', 'success')
        return redirect(url_for('routes.index'))
    else:
        flash('Ошибка авторизации через ВКонтакте', 'error')
        return redirect(url_for('auth.login'))

@routes_bp.route('/auth/yandex')
def yandex_login():
    """Авторизация через Яндекс"""
    redirect_uri = url_for('routes.yandex_callback', _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)

@routes_bp.route('/auth/yandex/callback')
def yandex_callback():
    """Callback для Яндекс"""
    user = handle_oauth_callback('yandex')
    if user:
        flash(f'Добро пожаловать, {user.username}!', 'success')
        return redirect(url_for('routes.index'))
    else:
        flash('Ошибка авторизации через Яндекс', 'error')
        return redirect(url_for('auth.login'))

@routes_bp.route('/test-images')
def test_images():
    """Тестовая страница для проверки изображений"""
    return render_template('test_images.html')

@routes_bp.route('/audio-settings')
def audio_settings():
    """Страница настроек аудио"""
    return render_template('audio_settings.html')

@routes_bp.route('/time-test')
def time_test():
    """Тестовая страница для проверки динамических цветов"""
    return render_template('time_test.html')

@routes_bp.route('/test-city-selector')
def test_city_selector():
    """Тестовая страница для проверки селектора городов"""
    return render_template('test_city_selector.html')

@routes_bp.route('/resumes')
@login_required
def resumes():
    page = request.args.get('page', 1, type=int)
    per_page = 6

    all_resumes = Resume.query.all()
    total = len(all_resumes)
    total_pages = ceil(total / per_page)
    
    start = (page - 1) * per_page
    end = start + per_page
    resumes_paginated = all_resumes[start:end]
    
    return render_template('resumes.html', resumes=resumes_paginated, page=page, total_pages=total_pages)

@routes_bp.route('/my_resumes')
@login_required
def my_resumes():
    # Получаем все резюме текущего пользователя из базы
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('my_resumes.html', resumes=resumes)

@routes_bp.route('/resume/add', methods=['GET', 'POST'])
@login_required
def add_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        filename = None
        file = request.files.get('photo_file')
        if file and file.filename:
            allowed_ext = {'jpg', 'jpeg', 'png'}
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext not in allowed_ext:
                flash('Разрешены только файлы JPG, JPEG, PNG.', 'danger')
                return render_template('resume_form.html', form=form, title='Добавить резюме')
            # Проверка размера
            file.seek(0, 2)
            size = file.tell()
            if size > app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024):
                flash('Файл слишком большой. Максимальный размер: 16MB', 'danger')
                file.seek(0)
                return render_template('resume_form.html', form=form, title='Добавить резюме')
            file.seek(0)
            # Проверка MIME-типа
            mime = file.mimetype
            if mime not in ['image/jpeg', 'image/png']:
                flash('Разрешены только изображения JPG или PNG.', 'danger')
                return render_template('resume_form.html', form=form, title='Добавить резюме')
            # Проверка содержимого файла через Pillow
            try:
                img = Image.open(BytesIO(file.read()))
                img.verify()
                file.seek(0)
                if img.format not in ['JPEG', 'PNG']:
                    flash('Файл должен быть JPG или PNG.', 'danger')
                    return render_template('resume_form.html', form=form, title='Добавить резюме')
            except Exception:
                flash('Файл повреждён или не является изображением.', 'danger')
                return render_template('resume_form.html', form=form, title='Добавить резюме')
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)

        new_resume = Resume(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data if form.age.data and str(form.age.data).isdigit() else None,
            phone_number=form.phone_number.data,
            email=form.email.data,
            description=form.description.data,
            photo_filename=filename,
            user_id=current_user.id
        )
        try:
            db.session.add(new_resume)
            db.session.commit()
            flash("Резюме добавлено.")
            return redirect(url_for('routes.profile'))
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при добавлении резюме.")
            print(e)
        else:
            print(form.errors)
    return render_template('resume_form.html', form=form, title='Добавить резюме')

@routes_bp.route('/resume/download/<int:resume_id>')
@login_required
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    if resume.user_id != current_user.id:
        abort(403)

    return send_from_directory('uploads', resume.photo_filename, as_attachment=True)

@routes_bp.route('/resume/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@owner_required(Resume)
def edit_resume(id):
    resume = Resume.query.get_or_404(id)
    form = ResumeForm(obj=resume)

    if form.validate_on_submit():
        file = request.files.get('photo_file')
        if file and file.filename:
            allowed_ext = {'jpg', 'jpeg', 'png'}
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext not in allowed_ext:
                flash('Разрешены только файлы JPG, JPEG, PNG.', 'danger')
                return render_template('resume_form.html', form=form, is_edit=True)
            file.seek(0, 2)
            size = file.tell()
            if size > app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024):
                flash('Файл слишком большой. Максимальный размер: 16MB', 'danger')
                file.seek(0)
                return render_template('resume_form.html', form=form, is_edit=True)
            file.seek(0)
            mime = file.mimetype
            if mime not in ['image/jpeg', 'image/png']:
                flash('Разрешены только изображения JPG или PNG.', 'danger')
                return render_template('resume_form.html', form=form, is_edit=True)
            try:
                img = Image.open(BytesIO(file.read()))
                img.verify()
                file.seek(0)
                if img.format not in ['JPEG', 'PNG']:
                    flash('Файл должен быть JPG или PNG.', 'danger')
                    return render_template('resume_form.html', form=form, is_edit=True)
            except Exception:
                flash('Файл повреждён или не является изображением.', 'danger')
                return render_template('resume_form.html', form=form, is_edit=True)
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            full_path = os.path.join(upload_folder, filename)
            os.makedirs(upload_folder, exist_ok=True)
            file.save(full_path)

            if resume.photo_filename and resume.photo_filename != filename:
                old_path = os.path.join(upload_folder, resume.photo_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            resume.photo_filename = filename

        resume.name = form.name.data
        resume.surname = form.surname.data
        # Безопасная обработка возраста
        if form.age.data and str(form.age.data).isdigit():
            resume.age = int(form.age.data)
        else:
            resume.age = None
        resume.phone_number = form.phone_number.data
        resume.email = form.email.data
        resume.description = form.description.data
        try:
            db.session.commit()
            flash("Резюме обновлено.")
            return redirect(url_for('routes.resumes'))
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при обновлении резюме.")
            print(e)

    return render_template('resume_form.html', form=form, is_edit=True)

@routes_bp.route('/resume/<int:id>')
def resume_detail(id):
    resume = Resume.query.get_or_404(id)
    return render_template('resume_detail.html', resume=resume)

@routes_bp.route('/create_resume', methods=['GET', 'POST'])
@login_required
def create_resume():
    form = ResumeForm()

    if form.validate_on_submit():
        filename = None
        file = request.files.get('photo_file')
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)

        resume = Resume(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data if form.age.data and str(form.age.data).isdigit() else None,
            phone_number=form.phone_number.data,
            email=form.email.data,
            description=form.description.data,
            photo_filename=filename,
            user_id=current_user.id
        )
        db.session.add(resume)
        db.session.commit()
        flash('Резюме успешно создано', 'success')
        return redirect(url_for('routes.profile'))

    return render_template('resume_form.html', form=form)

@routes_bp.route('/resume/<int:id>/delete', methods=['POST'])
@login_required
@owner_required(Resume)
def delete_resume(id):
    resume = Resume.query.get_or_404(id)
    
    try:
        if resume.photo_filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], resume.photo_filename)
            if os.path.exists(path):
                os.remove(path)
        db.session.delete(resume)
        db.session.commit()
        flash("Резюме удалено.", 'success')
    except Exception as e:
        db.session.rollback()
        flash("Ошибка при удалении резюме.", 'danger')
        print(f"Delete resume error: {e}")
    return redirect(url_for('routes.profile'))


@routes_bp.route('/vacancy/<int:vacancy_id>/respond', methods=['POST'])
@login_required
def respond_to_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    message = request.form.get('message')
    resume_id = request.form.get('resume_id')

    if not message or not resume_id:
        flash('Заполните все поля', 'danger')
        return redirect(url_for('routes.vacancy_detail', id=vacancy_id))

    response = ResponseVacancy(
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        message=message,
        user_id=current_user.id
    )

    db.session.add(response)
    db.session.commit()

    notify_new_response(vacancy, message, current_user.email)
    flash('Ваш отклик отправлен', 'success')
    return redirect(url_for('routes.vacancy_detail', id=vacancy_id))

@routes_bp.route('/vacancy/add', methods=['GET', 'POST'])
@login_required
def add_vacancy():
    form = VacancyForm()
    if form.validate_on_submit():
        new_vacancy = Vacancy(
            title=form.title.data,
            city=form.city.data,
            experience=form.experience.data,
            direction=form.direction.data,
            description=form.description.data,
            salary_from=float(form.salary_from.data) if form.salary_from.data else None,
            salary_to=float(form.salary_to.data) if form.salary_to.data else None,
            
            user_id=current_user.id
        )
        try:
            db.session.add(new_vacancy)
            db.session.commit()
            flash("Вакансия добавлена")
            return redirect(url_for('routes.list_vacancies'))
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при добавлении вакансии: " + str(e))
    return render_template('vacancy_form.html', form=form, title="добавить вакансию")


@routes_bp.route('/vacancies', endpoint='vacancies')
def list_vacancies():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Vacancy.query.paginate(page=page, per_page=per_page, error_out=False)
    vacancies = pagination.items
    return render_template('vacancies.html', vacancies=vacancies, pagination=pagination, page=page)

@routes_bp.route('/my_vacancies')
@login_required
def my_vacancies():
    # Получаем список вакансий, принадлежащих текущему пользователю
    vacancies = Vacancy.query.filter_by(user_id=current_user.id).all()
    
    # Передаем список вакансий в шаблон
    return render_template('my_vacancies.html', vacancies=vacancies)

# Пример маршрута для удаления вакансии (для полноты)
@routes_bp.route('/delete_vacancy/<int:id>', methods=['POST'])
@login_required
def delete_vacancy(id):
    vacancy = Vacancy.query.get_or_404(id)
    # Проверяем, что текущий пользователь — автор вакансии
    if vacancy.user_id != current_user.id:
        flash('Нет прав для удаления этой вакансии.', 'danger')
        return redirect(url_for('routes.my_vacancies'))
    try:
        db.session.delete(vacancy)
        db.session.commit()
        flash('Вакансия удалена.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении вакансии.', 'danger')
    return redirect(url_for('routes.my_vacancies'))


@routes_bp.route('/vacancy/<int:id>')
def vacancy_detail(id):
    vacancy = Vacancy.query.get_or_404(id)
    responses = db.session.query(ResponseVacancy).filter_by(vacancy_id=id).all()

    user_authenticated = current_user.is_authenticated
    
    # Безопасное получение current_user_id
    current_user_id = None
    if user_authenticated:
        try:
            current_user_id = current_user.id
        except AttributeError:
            user_authenticated = False
            current_user_id = None
    
    # Получаем пользователей для откликов
    response_user_ids = [response.user_id for response in responses]
    users_dict = {user.id: user for user in User.query.filter(User.id.in_(response_user_ids)).all()}

    # Добавляем информацию о пользователях к откликам
    responses_with_users = []
    for response in responses:
        user = users_dict.get(response.user_id)
        if user:
            response.user = user
            responses_with_users.append(response)

    # Безопасная проверка владельца
    is_owner = False
    if user_authenticated:
        try:
            is_owner = (vacancy.user_id == current_user.id)
        except AttributeError:
            is_owner = False

    has_response = False
    if user_authenticated and current_user_id:
        has_response = any(response.user_id == current_user_id for response in responses)

    return render_template('vacancy_detail.html',
                           vacancy=vacancy,
                           responses=responses_with_users,
                           is_owner=is_owner,
                           has_response=has_response)

# Профили по ролям

@routes_bp.route('/profile')
@login_required
def profile():
    user = current_user
    resumes = Resume.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, resumes=resumes)

@routes_bp.route('/profile_candidate')
@login_required
def profile_candidate():
    if current_user.role != 'candidate':
        flash('Доступ запрещён: вы не кандидат', 'danger')
        return redirect(url_for('routes.profile'))
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('profile_candidate.html', user=current_user, resumes=resumes)

@routes_bp.route('/profile_employer')
@login_required
def profile_employer():
    if current_user.role != 'employer':
        flash('Доступ запрещён: вы не работодатель', 'danger')
        return redirect(url_for('routes.profile'))
    vacancies = Vacancy.query.filter_by(user_id=current_user.id).all()
    return render_template('profile_employer.html', user=current_user, vacancies=vacancies)

@routes_bp.route('/api/cities', methods=['GET'])
def get_cities():
    """Получить список всех городов"""
    cities = City.query.filter_by(is_active=True).order_by(City.sort_order.desc(), City.population.desc()).all()
    city_list = [{"id": city.id, "name": city.name, "region": city.region} for city in cities]
    return jsonify(cities=city_list)

@routes_bp.route('/api/cities/search', methods=['GET'])
def search_cities():
    """Поиск городов по названию"""
    query = request.args.get('q', '').strip()
    print(f"🔍 Поиск городов: '{query}'")
    
    if not query or len(query) < 2:
        print("❌ Запрос слишком короткий")
        return jsonify(cities=[])
    
    cities = City.search_cities(query, limit=10)
    city_list = [{"id": city.id, "name": city.name, "region": city.region} for city in cities]
    print(f"✅ Найдено городов: {len(city_list)}")
    print(f"📋 Результаты: {city_list}")
    
    return jsonify(cities=city_list)

@routes_bp.route('/api/cities/popular', methods=['GET'])
def get_popular_cities():
    """Получить популярные города"""
    limit = request.args.get('limit', 10, type=int)
    cities = City.get_popular_cities(limit)
    city_list = [{"id": city.id, "name": city.name, "region": city.region} for city in cities]
    return jsonify(cities=city_list)

@routes_bp.route('/set_role', methods=['POST'])
@login_required
def set_role():
    role = request.form.get('role')
    if role in ['candidate', 'employer']:
        current_user.role = role
        from extensions import db
        db.session.commit()
        flash('Роль успешно обновлена!', 'success')
        if role == 'candidate':
            return redirect(url_for('routes.profile_candidate'))
        else:
            return redirect(url_for('routes.profile_employer'))
    flash('Ошибка при выборе роли', 'danger')
    return redirect(url_for('routes.profile'))

@routes_bp.route('/profile/setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    if current_user.role and current_user.city and current_user.license_category and current_user.citizenship:
        # Если профиль уже заполнен, редиректим на профиль
        return redirect(url_for('routes.profile'))
    if request.method == 'POST':
        role = request.form.get('role')
        city = request.form.get('city')
        license_category = request.form.get('license_category')
        citizenship = request.form.get('citizenship')
        if not all([role, city, license_category, citizenship]):
            flash('Пожалуйста, заполните все поля', 'danger')
            return render_template('profile_setup.html')
        current_user.role = role
        current_user.city = city
        current_user.license_category = license_category
        current_user.citizenship = citizenship
        db.session.commit()
        # После заполнения — редирект на создание резюме или вакансии
        if role == 'employer':
            return redirect(url_for('routes.add_vacancy'))
        else:
            return redirect(url_for('routes.create_resume'))
    return render_template('profile_setup.html')