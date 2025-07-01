"""
Конфигурация для продакшена
"""
import os
from config import Config
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    
    # Отключаем режим отладки
    DEBUG = False
    TESTING = False
    
    # Обязательные настройки безопасности
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY должен быть установлен в продакшене!")
    
    # Настройки безопасности для продакшена
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Настройки CSRF
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Настройки загрузки файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Проверяем настройки почты
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    if not all([MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD]):
        print("⚠️  ВНИМАНИЕ: Настройки почты не полностью установлены!")
    
    # Настройки логирования
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Настройки для статических файлов
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 год
    
    # Дополнительные настройки безопасности
    PERMANENT_SESSION_LIFETIME = 3600  # 1 час
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True 