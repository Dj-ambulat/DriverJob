#!/usr/bin/env python3
"""
Скрипт для массового обновления названия сайта
"""
import os
import re

def update_file_content(file_path, old_name, new_name):
    """Обновляет содержимое файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем различные варианты названия
        replacements = [
            ('Drivers.RU', new_name),
            ('Drivers.ru', new_name),
            ('Drivers.Ru', new_name),
            ('DRIVERS.RU', new_name.upper()),
            ('drivers.ru', new_name.lower()),
            ('DriverJob', new_name.replace(' ', '')),
            ('driverjob', new_name.lower().replace(' ', '')),
            ('https://drivers.ru', 'https://roadfighters.ru'),
            ('http://drivers.ru', 'https://roadfighters.ru'),
        ]
        
        original_content = content
        for old, new in replacements:
            content = content.replace(old, new)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Обновлен: {file_path}")
            return True
        else:
            print(f"⏭️  Пропущен: {file_path} (нет изменений)")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обновлении {file_path}: {e}")
        return False

def update_site_name():
    """Основная функция обновления названия сайта"""
    print("🔄 Обновление названия сайта с 'Drivers.RU' на 'Road Fighters'...")
    
    old_name = "Drivers.RU"
    new_name = "Road Fighters"
    
    # Список файлов для обновления
    files_to_update = [
        # Основные файлы
        'README.md',
        'SETUP.md',
        'STYLING_GUIDE.md',
        'TROUBLESHOOTING.md',
        
        # Шаблоны
        'templates/login.html',
        'templates/register.html',
        'templates/reset_password.html',
        'templates/reset_password_request.html',
        'templates/profile.html',
        'templates/vacancies.html',
        'templates/vacancy_detail.html',
        'templates/my_vacancies.html',
        'templates/edit_vacancy.html',
        'templates/ad_vacancy.html',
        'templates/resumes.html',
        'templates/resume_detail.html',
        'templates/resume_form.html',
        'templates/my_resumes.html',
        'templates/403.html',
        'templates/404.html',
        'templates/500.html',
        'templates/auth_base.html',
        'templates/vacancy_form.html',
        
        # Шаблоны в подпапках
        'templates/авторизация/login.html',
        'templates/авторизация/register.html',
        'templates/авторизация/reset_password.html',
        'templates/авторизация/reset_request.html',
        'templates/вакансии/vacancies.html',
        'templates/вакансии/vacancy_detail.html',
        'templates/вакансии/my_vacancies.html',
        'templates/вакансии/edit_vacancy.html',
        'templates/вакансии/add_vacancy.html',
        'templates/ошибки/403.html',
        'templates/ошибки/404.html',
        'templates/ошибки/500.html',
        
        # Статические файлы
        'static/sitemap.xml',
        'static/images/site.webmanifest',
        
        # Документация
        'ENV_SETUP_INSTRUCTIONS.md',
        'SECRET_KEY_SETUP.md',
        'CODE_REVIEW_REPORT.md',
        'QUICK_DEPLOY.md',
        'beget_deploy.md',
    ]
    
    updated_count = 0
    total_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            total_count += 1
            if update_file_content(file_path, old_name, new_name):
                updated_count += 1
        else:
            print(f"⚠️  Файл не найден: {file_path}")
    
    print(f"\n📊 Результаты обновления:")
    print(f"✅ Обновлено файлов: {updated_count}")
    print(f"📁 Всего проверено: {total_count}")
    print(f"🎯 Название сайта изменено на: {new_name}")
    
    # Обновляем .env файл если он существует
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"\n🔧 Обновление {env_file}...")
        update_file_content(env_file, old_name, new_name)
    
    print(f"\n🎉 Обновление завершено! Теперь ваш сайт называется '{new_name}'")

if __name__ == '__main__':
    update_site_name() 