import os
import secrets

class Config:
    # Генерируем случайный секретный ключ если не установлен
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jobportal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки почты
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your_email_password'
    
    # Настройки загрузки файлов
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Дополнительные настройки безопасности
    WTF_CSRF_TIME_LIMIT = 3600  # 1 час для CSRF токенов
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # OAuth настройки
    VK_CLIENT_ID = os.environ.get('VK_CLIENT_ID')
    VK_CLIENT_SECRET = os.environ.get('VK_CLIENT_SECRET')
    YANDEX_CLIENT_ID = os.environ.get('YANDEX_CLIENT_ID')
    YANDEX_CLIENT_SECRET = os.environ.get('YANDEX_CLIENT_SECRET')
    
    # Google reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', 'your-public-key')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', 'your-secret-key')
    
    # Настройки для продакшена
    if os.environ.get('FLASK_ENV') == 'production':
        debug = False
        testing = False
        # В продакшене обязательно должны быть установлены переменные окружения
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY должен быть установлен в продакшене!")
        if not os.environ.get('MAIL_USERNAME') or not os.environ.get('MAIL_PASSWORD'):
            print("ВНИМАНИЕ: Настройки почты не установлены!")
    else:
        debug = True
        testing = False