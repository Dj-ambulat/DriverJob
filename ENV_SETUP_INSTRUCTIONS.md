# 📝 Инструкции по настройке файла .env

## 🔍 Анализ текущего состояния

Файл `.env` **отсутствует** в вашем проекте. Это нормально, так как он должен содержать секретные данные и не должен быть в репозитории.

## 🚀 Создание файла .env

### Шаг 1: Создайте файл .env

Создайте файл с именем `.env` (без расширения) в корне проекта `C:\RoadFighters\.env`

### Шаг 2: Добавьте содержимое

Скопируйте следующий код в файл `.env`:

```env
# Безопасность (ОБЯЗАТЕЛЬНО!)
SECRET_KEY=@+uT|zw^r](A6RJ&2;hy5OK+xY^E$Tn|0Y-x+Sfnad^!J&6,w8QX#I4ro6erJiS&

# Окружение
FLASK_ENV=production

# База данных
DATABASE_URL=sqlite:///jobportal.db

# Настройки почты (ЗАПОЛНИТЕ РЕАЛЬНЫМИ ДАННЫМИ!)
MAIL_SERVER=smtp.beget.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@домен.com
MAIL_PASSWORD=ваш_пароль_от_почты

# Настройки приложения
UPLOAD_FOLDER=uploads
SITE_URL=https://ваш_домен.com

# Настройки безопасности для продакшена
SESSION_COOKIE_SECURE=true
```

## ⚠️ Что нужно изменить в .env

### 1. Настройки почты (ОБЯЗАТЕЛЬНО!)

Замените следующие строки на реальные данные:

```env
# Если используете Gmail:
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=ваш_email@gmail.com
MAIL_PASSWORD=ваш_пароль_приложения

# Если используете Beget:
MAIL_SERVER=smtp.beget.com
MAIL_USERNAME=ваш_email@ваш_домен.com
MAIL_PASSWORD=ваш_пароль_от_почты

# Если используете Yandex:
MAIL_SERVER=smtp.yandex.ru
MAIL_USERNAME=ваш_email@yandex.ru
MAIL_PASSWORD=ваш_пароль_приложения
```

### 2. URL сайта (ОБЯЗАТЕЛЬНО!)

```env
# Замените на ваш реальный домен:
SITE_URL=https://ваш_домен.com
```

### 3. SECRET_KEY (ОПЦИОНАЛЬНО)

Если хотите сгенерировать новый SECRET_KEY:
```bash
python generate_secret_key.py
```

## 🔧 Проверка настроек

После создания файла `.env` запустите:

```bash
python check_production.py
```

Вы должны увидеть:
```
✅ Все проверки пройдены! Проект готов к продакшену.
```

## 📋 Полный список переменных

### Обязательные переменные:
- ✅ `SECRET_KEY` - секретный ключ (уже готов)
- ❌ `MAIL_USERNAME` - email для отправки писем
- ❌ `MAIL_PASSWORD` - пароль от email
- ❌ `SITE_URL` - URL вашего сайта

### Опциональные переменные:
- `MAIL_SERVER` - SMTP сервер (по умолчанию: smtp.beget.com)
- `MAIL_PORT` - порт SMTP (по умолчанию: 587)
- `MAIL_USE_TLS` - использование TLS (по умолчанию: true)
- `DATABASE_URL` - URL базы данных (по умолчанию: sqlite:///jobportal.db)
- `UPLOAD_FOLDER` - папка для загрузок (по умолчанию: uploads)

## 🎯 Примеры настроек для разных провайдеров

### Gmail:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@gmail.com
MAIL_PASSWORD=ваш_пароль_приложения
```

### Yandex:
```env
MAIL_SERVER=smtp.yandex.ru
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@yandex.ru
MAIL_PASSWORD=ваш_пароль_приложения
```

### Beget:
```env
MAIL_SERVER=smtp.beget.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@ваш_домен.com
MAIL_PASSWORD=ваш_пароль_от_почты
```

## 🚨 Важные замечания

1. **Никогда не коммитьте** файл `.env` в Git
2. **Храните резервную копию** настроек в безопасном месте
3. **Используйте разные** настройки для разработки и продакшена
4. **Для Gmail** используйте пароль приложения, а не обычный пароль

## ✅ После настройки

1. Создайте файл `.env` с настройками выше
2. Замените `ваш_email@домен.com` на реальный email
3. Замените `ваш_пароль_от_почты` на реальный пароль
4. Замените `https://ваш_домен.com` на реальный URL
5. Запустите `python check_production.py` для проверки 