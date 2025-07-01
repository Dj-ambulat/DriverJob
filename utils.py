from extensions import mail
from flask_mail import Message
from flask import current_app
from models import User
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, recipients, body):
    """Отправка email с обработкой ошибок"""
    try:
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = body
        mail.send(msg)
        logger.info(f"Email отправлен: {subject} -> {recipients}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")
        return False

def notify_new_response(vacancy, message, responder_email):
    """Уведомление о новом отклике на вакансию"""
    try:
        user = User.query.get(vacancy.user_id)
        if user and user.email:
            subject = f"Новый отклик на вакансию '{vacancy.title}'"
            body = f"""
Здравствуйте, {user.username}!

На вашу вакансию "{vacancy.title}" поступил новый отклик от {responder_email}.

Сообщение отклика:
{message}

С уважением,
Команда Road Fighters
            """
            return send_email(subject, [user.email], body)
        else:
            logger.warning(f"Пользователь {vacancy.user_id} не найден или не имеет email")
            return False
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о отклике: {e}")
        return False

def notify_new_vacancy(vacancy, notify_all=False):
    """Уведомление о новой вакансии (только подписчикам или всем)"""
    try:
        if notify_all:
            # Отправляем только работодателям или всем (с ограничением)
            users = User.query.filter(User.role == 'employer').limit(50).all()
        else:
            # В будущем здесь можно добавить систему подписок
            users = []
        
        if not users:
            logger.info("Нет пользователей для уведомления о новой вакансии")
            return True
            
        subject = f"Новая вакансия: {vacancy.title}"
        body = f"""
Здравствуйте!

Добавлена новая вакансия на сайте Road Fighters:

Название: {vacancy.title}
Город: {vacancy.city or 'Не указан'}
Опыт: {vacancy.experience or 'Не указан'}
Зарплата: {vacancy.salary_from or 'Не указана'} - {vacancy.salary_to or 'Не указана'}

Описание:
{vacancy.description[:200]}{'...' if len(vacancy.description) > 200 else ''}

Подробнее: {current_app.config.get('SITE_URL', 'http://localhost:5000')}/vacancy/{vacancy.id}

С уважением,
Команда Road Fighters
        """
        
        success_count = 0
        for user in users:
            if user.email and send_email(subject, [user.email], body):
                success_count += 1
        
        logger.info(f"Уведомления о новой вакансии отправлены: {success_count}/{len(users)}")
        return success_count > 0
        
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомлений о новой вакансии: {e}")
        return False

def log_security_event(event, details=None):
    logger = logging.getLogger('security')
    msg = f"[SECURITY] {event}"
    if details:
        msg += f" | {details}"
    logger.warning(msg)