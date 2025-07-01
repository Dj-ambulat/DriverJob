import datetime
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)  # Может быть null для OAuth пользователей
    
    # Поля для OAuth авторизации
    external_id = db.Column(db.String(100), unique=True, nullable=True)
    external_provider = db.Column(db.String(20), nullable=True)  # 'vk', 'yandex'
    avatar_url = db.Column(db.String(500), nullable=True)

    role = db.Column(db.String(20), nullable=False, default='candidate')

    resumes = db.relationship('Resume', backref='user', lazy=True)
    vacancies = db.relationship('Vacancy', backref='user', lazy=True)

    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirm_token = db.Column(db.String(128), nullable=True)

    city = db.Column(db.String(100), nullable=True)
    license_category = db.Column(db.String(20), nullable=True)
    citizenship = db.Column(db.String(100), nullable=True)

    @property
    def password(self):
        raise AttributeError('Пароль нельзя читать напрямую!')

    @password.setter
    def password(self, password_plaintext):
        self.password_hash = generate_password_hash(password_plaintext)

    def check_password(self, password_plaintext):
        return check_password_hash(self.password_hash, password_plaintext)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    position = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    photo_filename = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def email(self):
        """Получаем email из связанного пользователя"""
        return self.user.email if self.user else None
    
    @property
    def full_name(self):
        """Полное имя резюме"""
        return f"{self.name} {self.surname}"
    
    def __repr__(self):
        return f'<Resume {self.full_name}>'

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)               # Название вакансии
    description = db.Column(db.Text, nullable=False)                # Описание
    city = db.Column(db.String(100), nullable=True)                 # Город
    experience = db.Column(db.String(100), nullable=True)           # Опыт
    direction = db.Column(db.String(100), nullable=True)            # Направление
    salary_from = db.Column(db.Integer, nullable=True)              # Зарплата от
    salary_to = db.Column(db.Integer, nullable=True)                # Зарплата до
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Дата создания
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Владелец
    responses = db.relationship('ResponseVacancy', backref='vacancy', lazy=True)  # Отклики
    
    @property
    def salary_range(self):
        """Возвращает диапазон зарплаты в читаемом виде"""
        if self.salary_from and self.salary_to:
            return f"{self.salary_from:,} - {self.salary_to:,} ₽"
        elif self.salary_from:
            return f"от {self.salary_from:,} ₽"
        elif self.salary_to:
            return f"до {self.salary_to:,} ₽"
        else:
            return "По договоренности"
    
    def __repr__(self):
        return f'<Vacancy {self.title}>'

class ResponseVacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Добавляем связи для удобства
    resume = db.relationship('Resume', backref='responses')
    user = db.relationship('User', backref='responses')

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Добавляем связь с пользователем
    user = db.relationship('User', backref='password_reset_tokens')

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    region = db.Column(db.String(100), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<City {self.name}>'
    
    @classmethod
    def get_popular_cities(cls, limit=10):
        """Получить популярные города"""
        return cls.query.filter_by(is_active=True).order_by(cls.sort_order.desc(), cls.population.desc()).limit(limit).all()
    
    @classmethod
    def search_cities(cls, query, limit=20):
        """Поиск городов по названию"""
        return cls.query.filter(
            cls.is_active == True,
            cls.name.ilike(f'%{query}%')
        ).order_by(cls.population.desc()).limit(limit).all()