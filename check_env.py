#!/usr/bin/env python3
"""
Скрипт для проверки настроек .env файла
"""
import os
from load_env import load_environment

def check_env_settings():
    """Проверка настроек .env файла"""
    print("🔍 Проверка настроек .env файла...")
    
    # Загружаем переменные окружения
    load_environment()
    
    print("\n" + "="*60)
    print("📋 ТЕКУЩИЕ НАСТРОЙКИ:")
    print("="*60)
    
    # Проверяем каждую переменную
    settings = {
        'SECRET_KEY': {
            'required': True,
            'description': 'Секретный ключ для безопасности',
            'current': os.environ.get('SECRET_KEY', 'НЕ УСТАНОВЛЕН'),
            'status': '❌' if not os.environ.get('SECRET_KEY') else '✅'
        },
        'FLASK_ENV': {
            'required': True,
            'description': 'Окружение приложения',
            'current': os.environ.get('FLASK_ENV', 'development'),
            'status': '⚠️' if os.environ.get('FLASK_ENV') != 'production' else '✅'
        },
        'MAIL_SERVER': {
            'required': False,
            'description': 'SMTP сервер для отправки писем',
            'current': os.environ.get('MAIL_SERVER', 'smtp.example.com (по умолчанию)'),
            'status': '⚠️' if os.environ.get('MAIL_SERVER') == 'smtp.example.com' else '✅'
        },
        'MAIL_USERNAME': {
            'required': True,
            'description': 'Email для отправки писем',
            'current': os.environ.get('MAIL_USERNAME', 'НЕ УСТАНОВЛЕН'),
            'status': '❌' if not os.environ.get('MAIL_USERNAME') or 'example' in os.environ.get('MAIL_USERNAME', '') else '✅'
        },
        'MAIL_PASSWORD': {
            'required': True,
            'description': 'Пароль от email',
            'current': os.environ.get('MAIL_PASSWORD', 'НЕ УСТАНОВЛЕН'),
            'status': '❌' if not os.environ.get('MAIL_PASSWORD') or 'password' in os.environ.get('MAIL_PASSWORD', '') else '✅'
        },
        'SITE_URL': {
            'required': True,
            'description': 'URL вашего сайта',
            'current': os.environ.get('SITE_URL', 'http://localhost:5000 (по умолчанию)'),
            'status': '⚠️' if 'localhost' in os.environ.get('SITE_URL', '') else '✅'
        },
        'DATABASE_URL': {
            'required': False,
            'description': 'URL базы данных',
            'current': os.environ.get('DATABASE_URL', 'sqlite:///jobportal.db (по умолчанию)'),
            'status': '✅'
        },
        'UPLOAD_FOLDER': {
            'required': False,
            'description': 'Папка для загрузок',
            'current': os.environ.get('UPLOAD_FOLDER', 'uploads (по умолчанию)'),
            'status': '✅'
        },
        'SESSION_COOKIE_SECURE': {
            'required': False,
            'description': 'Безопасные куки',
            'current': os.environ.get('SESSION_COOKIE_SECURE', 'false (по умолчанию)'),
            'status': '⚠️' if os.environ.get('SESSION_COOKIE_SECURE') != 'true' else '✅'
        }
    }
    
    # Выводим статус каждой настройки
    for key, info in settings.items():
        print(f"{info['status']} {key}: {info['current']}")
        print(f"   📝 {info['description']}")
        if info['required'] and info['status'] == '❌':
            print(f"   ⚠️  ОБЯЗАТЕЛЬНО для продакшена!")
        print()
    
    # Подсчитываем статистику
    total = len(settings)
    ok = sum(1 for info in settings.values() if info['status'] == '✅')
    warning = sum(1 for info in settings.values() if info['status'] == '⚠️')
    error = sum(1 for info in settings.values() if info['status'] == '❌')
    
    print("="*60)
    print("📊 СТАТИСТИКА:")
    print(f"✅ Правильно настроено: {ok}/{total}")
    print(f"⚠️  Требует внимания: {warning}/{total}")
    print(f"❌ Не настроено: {error}/{total}")
    print("="*60)
    
    # Рекомендации
    print("\n🎯 РЕКОМЕНДАЦИИ:")
    
    if error > 0:
        print("❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ:")
        for key, info in settings.items():
            if info['status'] == '❌':
                print(f"   - Настройте {key}")
    
    if warning > 0:
        print("⚠️  РЕКОМЕНДУЕМЫЕ УЛУЧШЕНИЯ:")
        for key, info in settings.items():
            if info['status'] == '⚠️':
                print(f"   - Проверьте {key}")
    
    if error == 0 and warning == 0:
        print("✅ Все настройки в порядке!")
    
    print("\n📝 СЛЕДУЮЩИЕ ШАГИ:")
    if error > 0:
        print("1. Создайте файл .env в корне проекта")
        print("2. Добавьте недостающие настройки")
        print("3. Запустите этот скрипт снова")
    else:
        print("1. Проект готов к развертыванию!")
        print("2. Запустите python check_production.py для финальной проверки")

if __name__ == '__main__':
    check_env_settings() 