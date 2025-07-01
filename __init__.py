from flask import Flask, render_template, request
from config import Config
from production_config import ProductionConfig
from extensions import db, csrf, mail, login_manager, limiter
from routes import routes_bp
from auth import auth_bp
from models import User
from flask_login import current_user
from oauth import init_oauth
import logging
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

def create_app():
    app = Flask(__name__)
    
    # Выбираем конфигурацию в зависимости от окружения
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
        app.logger.info("Используется продакшен конфигурация")
    else:
        app.config.from_object(Config)
        app.logger.info("Используется разработческая конфигурация")

    # Инициализация расширений
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Инициализация OAuth
    init_oauth(app)

    # Регистрация blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            app.logger.warning(f"Неверный user_id: {user_id}")
            return None
    
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.warning(f"403 ошибка: {error}")
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.info(f"404 ошибка: {request.url}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 ошибка: {error}")
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Необработанная ошибка: {e}")
        db.session.rollback()
        return render_template('500.html'), 500

    # Создание папок если их нет
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        app.logger.info(f"Создана папка: {upload_folder}")

    # Создание таблиц базы данных только в разработке
    if app.config.get('DEBUG', False):
        with app.app_context():
            try:
                db.create_all()
                app.logger.info("База данных инициализирована")
            except Exception as e:
                app.logger.error(f"Ошибка при создании таблиц: {e}")

    return app