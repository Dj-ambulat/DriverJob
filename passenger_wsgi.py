"""
WSGI файл для развертывания на Beget хостинге
"""
import os
import sys

# Добавляем путь к проекту в sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Устанавливаем переменную окружения для продакшена
os.environ['FLASK_ENV'] = 'production'

# Импортируем приложение
from __init__ import create_app
from load_env import load_environment

# Загружаем переменные окружения
load_environment()

# Создаем приложение
application = create_app()

# Для совместимости с некоторыми WSGI серверами
app = application 