"""
Модуль для загрузки переменных окружения
"""
import os
from dotenv import load_dotenv

def load_environment():
    """Загружает переменные окружения из файла .env"""
    # Ищем файл .env в корневой директории проекта
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("Переменные окружения загружены из .env")
    else:
        print("Файл .env не найден. Используются значения по умолчанию.")
        print("Создайте файл .env на основе env_example.txt")

if __name__ == '__main__':
    load_environment() 