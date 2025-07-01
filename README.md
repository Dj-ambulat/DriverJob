# Road Fighters - Платформа для поиска работы водителей

## 🚀 Описание

**Road Fighters** - это современная веб-платформа для поиска работы водителей и размещения вакансий. Сайт предоставляет удобный интерфейс для соискателей и работодателей в сфере грузоперевозок.

## ✨ Основные возможности

### Для водителей:
- 📝 Создание и редактирование резюме
- 🔍 Поиск вакансий по городу и категориям
- 📧 Отклики на вакансии с сообщениями
- 👤 Личный кабинет с управлением резюме

### Для работодателей:
- 📋 Размещение вакансий
- 👥 Просмотр откликов на вакансии
- 📊 Управление своими вакансиями
- 📧 Уведомления о новых откликах

## 🛠 Технологии

- **Backend:** Python Flask
- **Database:** SQLite (с возможностью перехода на PostgreSQL/MySQL)
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Email:** Flask-Mail
- **Security:** CSRF защита, хеширование паролей

## 📁 Структура проекта

```
Road Fighters/
├── __init__.py              # Фабрика приложения
├── config.py               # Конфигурация
├── models.py               # Модели базы данных
├── routes.py               # Маршруты приложения
├── auth.py                 # Аутентификация
├── forms.py                # Формы
├── utils.py                # Утилиты
├── extensions.py           # Расширения Flask
├── templates/              # HTML шаблоны
├── static/                 # Статические файлы
├── uploads/                # Загруженные файлы
├── requirements.txt        # Зависимости
└── run.py                  # Точка входа
```

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd Road Fighters
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` на основе `env_example.txt`:
```env
SECRET_KEY=ваш_секретный_ключ
FLASK_ENV=development
DATABASE_URL=sqlite:///jobportal.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@gmail.com
MAIL_PASSWORD=ваш_пароль_приложения
```

### 5. Инициализация базы данных
```bash
python init_db.py
python init_cities.py
```

### 6. Запуск приложения
```bash
python run.py
```

Приложение будет доступно по адресу: http://localhost:5000

## 📁 Файлы-заглушки

В проекте используются файлы-заглушки для следующих ресурсов:

### 🎵 Аудио файлы (`static/audio/`)
- `background-music.mp3` - фоновая музыка (MP3)
- `background-music.ogg` - фоновая музыка (OGG)
- **Инструкции**: `static/audio/README.md`

### 🖼️ Изображения контента (`static/images/content/`)
- `hero-truck.jpg` - главное изображение (800x600px)
- `no-vacancies.jpg` - изображение "нет вакансий" (400x300px)
- `truck-work.jpg` - изображение для карточек вакансий (400x300px)
- **Инструкции**: `static/images/content/README.md`

### 📝 Замена заглушек
1. Замените файлы-заглушки на реальные ресурсы
2. Следуйте инструкциям в соответствующих README файлах
3. Перезапустите сервер

**Примечание**: Заглушки позволяют запустить проект без ошибок 404, но для полноценной работы рекомендуется заменить их на реальные файлы.

## 📧 Настройка почты

Для работы уведомлений настройте SMTP в файле `.env`:

### Gmail:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@gmail.com
MAIL_PASSWORD=пароль_приложения
```

### Yandex:
```env
MAIL_SERVER=smtp.yandex.ru
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=ваш_email@yandex.ru
MAIL_PASSWORD=пароль_приложения
```

## 🚀 Развертывание на продакшене

### Beget хостинг:
1. Загрузите файлы на хостинг
2. Настройте Python приложение в панели Beget
3. Установите зависимости: `pip install -r requirements.txt`
4. Инициализируйте БД: `python init_db.py`
5. Настройте `.env` для продакшена

Подробные инструкции в файле `beget_deploy.md`

## 🔒 Безопасность

- ✅ CSRF защита для всех форм
- ✅ Хеширование паролей (Werkzeug)
- ✅ Безопасные сессии
- ✅ Валидация входных данных
- ✅ Защита от SQL-инъекций (SQLAlchemy)

## 📊 База данных

### Основные модели:
- **User** - пользователи (водители/работодатели)
- **Resume** - резюме водителей
- **Vacancy** - вакансии
- **ResponseVacancy** - отклики на вакансии
- **PasswordResetToken** - токены сброса пароля

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 📞 Поддержка

- Email: info@roadfighters.ru
- Сайт: https://roadfighters.ru

## 🧪 Тестовые аккаунты и данные

Для тестирования используйте следующие аккаунты:

- Email: test1@roadfighters.ru  |  Пароль: test1234
- Email: test2@roadfighters.ru  |  Пароль: test1234

В базе уже есть несколько тестовых вакансий и резюме для проверки интерфейса.

Если нужно сбросить тестовые данные — используйте скрипт `init_db.py` или обратитесь к администратору.

---

**Road Fighters** - лучшая платформа для поиска работы водителей! 🚛💨 