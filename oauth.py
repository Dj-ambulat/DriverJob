from authlib.integrations.flask_client import OAuth
from flask import current_app, url_for, session, redirect, request
import requests
from models import User, db
from flask_login import login_user
import os

oauth = OAuth()

def init_oauth(app):
    """Инициализация OAuth клиентов"""
    oauth.init_app(app)
    
    # ВКонтакте OAuth
    oauth.register(
        name='vk',
        client_id=app.config.get('VK_CLIENT_ID'),
        client_secret=app.config.get('VK_CLIENT_SECRET'),
        access_token_url='https://oauth.vk.com/access_token',
        access_token_params=None,
        authorize_url='https://oauth.vk.com/authorize',
        authorize_params=None,
        api_base_url='https://api.vk.com/method/',
        client_kwargs={'scope': 'email'},
    )
    
    # Яндекс OAuth
    oauth.register(
        name='yandex',
        client_id=app.config.get('YANDEX_CLIENT_ID'),
        client_secret=app.config.get('YANDEX_CLIENT_SECRET'),
        access_token_url='https://oauth.yandex.ru/token',
        access_token_params=None,
        authorize_url='https://oauth.yandex.ru/authorize',
        authorize_params=None,
        api_base_url='https://login.yandex.ru/info',
        client_kwargs={'scope': 'login:email login:info'},
    )

def get_vk_user_info(token):
    """Получение информации о пользователе ВКонтакте"""
    try:
        # Получаем информацию о пользователе
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': token['access_token'],
                'fields': 'photo_100,email',
                'v': '5.131'
            }
        )
        data = response.json()
        
        if 'response' in data and data['response']:
            user_data = data['response'][0]
            return {
                'id': f"vk_{user_data['id']}",
                'username': f"{user_data['first_name']} {user_data['last_name']}",
                'email': token.get('email', ''),
                'avatar': user_data.get('photo_100', ''),
                'provider': 'vk'
            }
    except Exception as e:
        current_app.logger.error(f"Ошибка получения данных ВКонтакте: {e}")
    return None

def get_yandex_user_info(token):
    """Получение информации о пользователе Яндекс"""
    try:
        # Получаем информацию о пользователе
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f"OAuth {token['access_token']}"}
        )
        data = response.json()
        
        return {
            'id': f"yandex_{data['id']}",
            'username': f"{data['first_name']} {data['last_name']}",
            'email': data.get('default_email', ''),
            'avatar': data.get('avatar_url', ''),
            'provider': 'yandex'
        }
    except Exception as e:
        current_app.logger.error(f"Ошибка получения данных Яндекс: {e}")
    return None

def create_or_get_user(user_info):
    """Создание или получение пользователя"""
    if not user_info:
        return None
    
    # Ищем пользователя по внешнему ID
    user = User.query.filter_by(external_id=user_info['id']).first()
    
    if not user:
        # Создаем нового пользователя
        user = User(
            username=user_info['username'],
            email=user_info['email'],
            external_id=user_info['id'],
            external_provider=user_info['provider'],
            avatar_url=user_info.get('avatar', '')
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"Создан новый пользователь через {user_info['provider']}: {user.username}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Ошибка создания пользователя: {e}")
            return None
    
    return user

def handle_oauth_callback(provider):
    """Обработка OAuth callback"""
    try:
        if provider == 'vk':
            token = oauth.vk.authorize_access_token()
            user_info = get_vk_user_info(token)
        elif provider == 'yandex':
            token = oauth.yandex.authorize_access_token()
            user_info = get_yandex_user_info(token)
        else:
            return None
        
        user = create_or_get_user(user_info)
        if user:
            login_user(user)
            return user
        
    except Exception as e:
        current_app.logger.error(f"Ошибка OAuth callback для {provider}: {e}")
    
    return None 