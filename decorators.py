from functools import wraps
from flask import abort
from flask_login import current_user

def owner_required(model_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Проверяем, что пользователь авторизован
            if not current_user.is_authenticated:
                abort(401)
            
            # Получаем id из kwargs
            item_id = kwargs.get('id')
            if not item_id:
                abort(400)
            
            # Получаем объект из базы данных
            item = model_class.query.get_or_404(item_id)
            
            # Проверяем, что текущий пользователь является владельцем
            try:
                if item.user_id != current_user.id:
                    abort(403)
            except AttributeError:
                abort(401)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator