"""
Точка входа в приложение
"""
from __init__ import create_app
from load_env import load_environment

# Загружаем переменные окружения
load_environment()

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    print("🚀 Запуск приложения Road Fighters...")
    print("📧 Для работы уведомлений настройте переменные окружения в файле .env")
    print("🌐 Приложение доступно по адресу: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)