#!/usr/bin/env python3
"""
Скрипт для генерации безопасного SECRET_KEY
"""
import secrets
import string

def generate_secret_key(length=64):
    """Генерирует безопасный секретный ключ"""
    # Используем буквы, цифры и специальные символы
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Генерируем случайную строку
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    
    return secret_key

def generate_hex_secret_key(length=64):
    """Генерирует секретный ключ в hex формате"""
    return secrets.token_hex(length // 2)

if __name__ == '__main__':
    print("🔐 Генерация SECRET_KEY для продакшена")
    print("=" * 50)
    
    # Генерируем несколько вариантов
    print("\n1️⃣ Сложный SECRET_KEY (рекомендуется):")
    secret_key = generate_secret_key(64)
    print(f"SECRET_KEY={secret_key}")
    
    print("\n2️⃣ Hex SECRET_KEY (альтернативный вариант):")
    hex_secret_key = generate_hex_secret_key(64)
    print(f"SECRET_KEY={hex_secret_key}")
    
    print("\n3️⃣ Короткий SECRET_KEY (для тестирования):")
    short_secret_key = generate_secret_key(32)
    print(f"SECRET_KEY={short_secret_key}")
    
    print("\n" + "=" * 50)
    print("📝 ИНСТРУКЦИИ:")
    print("1. Скопируйте один из SECRET_KEY выше")
    print("2. Создайте файл .env в корне проекта")
    print("3. Добавьте строку: SECRET_KEY=ваш_ключ")
    print("4. Убедитесь, что файл .env добавлен в .gitignore")
    print("\n⚠️  ВАЖНО:")
    print("- Никогда не коммитьте .env файл в Git")
    print("- Используйте разные ключи для разработки и продакшена")
    print("- Минимальная длина: 32 символа")
    print("- Рекомендуемая длина: 64 символа")
    
    print("\n🔒 Пример .env файла:")
    print("SECRET_KEY=" + secret_key)
    print("FLASK_ENV=production")
    print("DATABASE_URL=sqlite:///jobportal.db")
    print("MAIL_SERVER=smtp.beget.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=true")
    print("MAIL_USERNAME=ваш_email@домен.com")
    print("MAIL_PASSWORD=ваш_пароль")
    print("SITE_URL=https://ваш_домен.com")
    print("SESSION_COOKIE_SECURE=true") 