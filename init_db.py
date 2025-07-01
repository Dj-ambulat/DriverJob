#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных на продакшене
"""
import os
import sys
from __init__ import create_app
from models import db, User, Vacancy, Resume
from load_env import load_environment

def init_database():
    """Инициализация базы данных"""
    print("🔧 Инициализация базы данных...")
    
    # Загружаем переменные окружения
    load_environment()
    
    # Создаем приложение
    app = create_app()
    
    with app.app_context():
        try:
            # Создаем все таблицы
            db.create_all()
            print("✅ Таблицы базы данных созданы успешно!")
            
            # Проверяем, есть ли уже данные
            if User.query.first() is None:
                print("📝 База данных пуста. Готово к использованию.")
            else:
                print("📊 В базе данных уже есть данные.")
                
        except Exception as e:
            print(f"❌ Ошибка при создании базы данных: {e}")
            return False
    
    print("🎉 Инициализация завершена!")
    return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1) 