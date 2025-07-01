#!/usr/bin/env python3
"""
Скрипт для проверки готовности к продакшену
"""
import os
import sys
from load_env import load_environment

def check_production_readiness():
    """Проверка готовности к продакшену"""
    print("🔍 Проверка готовности к продакшену...")
    
    # Загружаем переменные окружения
    load_environment()
    
    issues = []
    warnings = []
    
    # Проверка обязательных переменных
    required_vars = [
        'SECRET_KEY',
        'FLASK_ENV',
        'MAIL_SERVER',
        'MAIL_USERNAME',
        'MAIL_PASSWORD'
    ]
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            issues.append(f"❌ Отсутствует обязательная переменная: {var}")
        elif var == 'SECRET_KEY' and len(value) < 32:
            issues.append(f"❌ SECRET_KEY слишком короткий (минимум 32 символа)")
        elif var == 'FLASK_ENV' and value != 'production':
            warnings.append(f"⚠️  FLASK_ENV установлен как '{value}', рекомендуется 'production'")
    
    # Проверка файлов
    required_files = [
        'passenger_wsgi.py',
        '.htaccess',
        'requirements.txt',
        '.env'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            issues.append(f"❌ Отсутствует файл: {file}")
    
    # Проверка папок
    required_dirs = [
        'uploads',
        'static',
        'templates'
    ]
    
    for dir in required_dirs:
        if not os.path.exists(dir):
            issues.append(f"❌ Отсутствует папка: {dir}")
    
    # Проверка прав доступа
    if os.path.exists('uploads'):
        if not os.access('uploads', os.W_OK):
            warnings.append("⚠️  Папка 'uploads' недоступна для записи")
    
    # Проверка .env файла
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_' in content or 'example' in content:
                warnings.append("⚠️  В .env файле есть примеры значений, замените на реальные")
    
    # Вывод результатов
    print("\n" + "="*50)
    
    if issues:
        print("❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ:")
        for issue in issues:
            print(f"  {issue}")
        print()
    
    if warnings:
        print("⚠️  ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    if not issues and not warnings:
        print("✅ Все проверки пройдены! Проект готов к продакшену.")
        return True
    elif not issues:
        print("✅ Критических проблем нет, но есть предупреждения.")
        return True
    else:
        print("❌ Есть критические проблемы, которые нужно исправить перед развертыванием.")
        return False

if __name__ == '__main__':
    success = check_production_readiness()
    sys.exit(0 if success else 1) 