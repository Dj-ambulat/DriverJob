# 🚀 Быстрое развертывание на BEGET.COM

## Шаг 1: Подготовка файлов

1. **Создайте файл `.env`** в корне проекта:
```env
SECRET_KEY=ваш_сложный_ключ_минимум_32_символа
FLASK_ENV=production
DATABASE_URL=sqlite:///jobportal.db
MAIL_SERVER=smtp.beget.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@домен.com
MAIL_PASSWORD=пароль_от_почты
SITE_URL=https://ваш_домен.com
SESSION_COOKIE_SECURE=true
```

## Шаг 2: Загрузка на хостинг

1. **Войдите в панель Beget**
2. **Откройте File Manager**
3. **Загрузите ВСЕ файлы** в корень домена
4. **Убедитесь, что `.env` загружен** (скрытый файл)

## Шаг 3: Настройка Python

1. **В панели Beget** → **Python**
2. **Создайте приложение**:
   - Python версия: 3.9+
   - Файл: `passenger_wsgi.py`
   - Домены: ваш домен

## Шаг 4: Установка зависимостей

**Через SSH или терминал:**
```bash
cd /path/to/your/site
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Шаг 5: Инициализация БД

```bash
source venv/bin/activate
python init_db.py
```

## Шаг 6: Проверка

Откройте ваш сайт в браузере!

## ⚠️ Важные моменты

- **SECRET_KEY** должен быть сложным и уникальным
- **Права доступа**: `chmod 755 uploads/`
- **Логи**: проверяйте в панели Beget при ошибках
- **SSL**: настройте в панели Beget

## 🔧 Если что-то не работает

1. Проверьте логи в панели Beget
2. Убедитесь, что `.env` файл загружен
3. Проверьте права доступа к папкам
4. Убедитесь, что Python приложение создано правильно

## 📞 Поддержка

- Техподдержка Beget: https://beget.com/ru/support
- Документация Flask: https://flask.palletsprojects.com/ 