#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для инициализации городов России в базе данных
"""

from __init__ import create_app
from extensions import db
from models import City

def init_cities():
    """Инициализация городов России"""
    
    # Список популярных городов России с населением
    cities_data = [
        # Москва и область
        {"name": "Москва", "region": "Московская область", "population": 12506468, "sort_order": 100},
        {"name": "Подольск", "region": "Московская область", "population": 309250, "sort_order": 90},
        {"name": "Химки", "region": "Московская область", "population": 257128, "sort_order": 89},
        {"name": "Балашиха", "region": "Московская область", "population": 520962, "sort_order": 88},
        {"name": "Королёв", "region": "Московская область", "population": 222952, "sort_order": 87},
        
        # Санкт-Петербург и область
        {"name": "Санкт-Петербург", "region": "Ленинградская область", "population": 5384342, "sort_order": 99},
        {"name": "Гатчина", "region": "Ленинградская область", "population": 94377, "sort_order": 85},
        {"name": "Выборг", "region": "Ленинградская область", "population": 77222, "sort_order": 84},
        
        # Центральный федеральный округ
        {"name": "Воронеж", "region": "Воронежская область", "population": 1057681, "sort_order": 86},
        {"name": "Ярославль", "region": "Ярославская область", "population": 608353, "sort_order": 85},
        {"name": "Рязань", "region": "Рязанская область", "population": 537622, "sort_order": 84},
        {"name": "Липецк", "region": "Липецкая область", "population": 503216, "sort_order": 83},
        {"name": "Тула", "region": "Тульская область", "population": 473622, "sort_order": 82},
        {"name": "Курск", "region": "Курская область", "population": 449556, "sort_order": 81},
        {"name": "Тверь", "region": "Тверская область", "population": 416219, "sort_order": 80},
        {"name": "Иваново", "region": "Ивановская область", "population": 401505, "sort_order": 79},
        {"name": "Брянск", "region": "Брянская область", "population": 399579, "sort_order": 78},
        {"name": "Белгород", "region": "Белгородская область", "population": 391554, "sort_order": 77},
        {"name": "Владимир", "region": "Владимирская область", "population": 356168, "sort_order": 76},
        {"name": "Архангельск", "region": "Архангельская область", "population": 351488, "sort_order": 75},
        {"name": "Калуга", "region": "Калужская область", "population": 337058, "sort_order": 74},
        {"name": "Смоленск", "region": "Смоленская область", "population": 320170, "sort_order": 73},
        {"name": "Орёл", "region": "Орловская область", "population": 303169, "sort_order": 72},
        {"name": "Кострома", "region": "Костромская область", "population": 277393, "sort_order": 71},
        {"name": "Тамбов", "region": "Тамбовская область", "population": 261803, "sort_order": 70},
        {"name": "Киров", "region": "Кировская область", "population": 501468, "sort_order": 69},
        
        # Приволжский федеральный округ
        {"name": "Нижний Новгород", "region": "Нижегородская область", "population": 1244254, "sort_order": 95},
        {"name": "Казань", "region": "Республика Татарстан", "population": 1251961, "sort_order": 94},
        {"name": "Самара", "region": "Самарская область", "population": 1164685, "sort_order": 93},
        {"name": "Уфа", "region": "Республика Башкортостан", "population": 1125698, "sort_order": 92},
        {"name": "Пермь", "region": "Пермский край", "population": 1048005, "sort_order": 91},
        {"name": "Саратов", "region": "Саратовская область", "population": 830155, "sort_order": 90},
        {"name": "Тольятти", "region": "Самарская область", "population": 685619, "sort_order": 89},
        {"name": "Ижевск", "region": "Удмуртская Республика", "population": 646277, "sort_order": 88},
        {"name": "Ульяновск", "region": "Ульяновская область", "population": 624518, "sort_order": 87},
        {"name": "Чебоксары", "region": "Чувашская Республика", "population": 495810, "sort_order": 86},
        {"name": "Пенза", "region": "Пензенская область", "population": 520300, "sort_order": 85},
        {"name": "Набережные Челны", "region": "Республика Татарстан", "population": 532074, "sort_order": 84},
        {"name": "Ростов-на-Дону", "region": "Ростовская область", "population": 1137704, "sort_order": 96},
        {"name": "Волгоград", "region": "Волгоградская область", "population": 1015587, "sort_order": 95},
        {"name": "Краснодар", "region": "Краснодарский край", "population": 974319, "sort_order": 94},
        {"name": "Астрахань", "region": "Астраханская область", "population": 524371, "sort_order": 83},
        {"name": "Ставрополь", "region": "Ставропольский край", "population": 450680, "sort_order": 82},
        {"name": "Сочи", "region": "Краснодарский край", "population": 411524, "sort_order": 81},
        {"name": "Волжский", "region": "Волгоградская область", "population": 321479, "sort_order": 80},
        {"name": "Новороссийск", "region": "Краснодарский край", "population": 275197, "sort_order": 79},
        {"name": "Шахты", "region": "Ростовская область", "population": 235492, "sort_order": 78},
        {"name": "Новочеркасск", "region": "Ростовская область", "population": 168746, "sort_order": 77},
        {"name": "Таганрог", "region": "Ростовская область", "population": 248664, "sort_order": 76},
        {"name": "Анапа", "region": "Краснодарский край", "population": 81947, "sort_order": 75},
        
        # Уральский федеральный округ
        {"name": "Екатеринбург", "region": "Свердловская область", "population": 1544376, "sort_order": 97},
        {"name": "Челябинск", "region": "Челябинская область", "population": 1189525, "sort_order": 96},
        {"name": "Тюмень", "region": "Тюменская область", "population": 847488, "sort_order": 95},
        {"name": "Магнитогорск", "region": "Челябинская область", "population": 410594, "sort_order": 84},
        {"name": "Нижний Тагил", "region": "Свердловская область", "population": 344656, "sort_order": 83},
        {"name": "Курган", "region": "Курганская область", "population": 309285, "sort_order": 82},
        {"name": "Сургут", "region": "Ханты-Мансийский автономный округ", "population": 387235, "sort_order": 81},
        {"name": "Нижневартовск", "region": "Ханты-Мансийский автономный округ", "population": 283256, "sort_order": 80},
        {"name": "Новый Уренгой", "region": "Ямало-Ненецкий автономный округ", "population": 118115, "sort_order": 79},
        
        # Сибирский федеральный округ
        {"name": "Новосибирск", "region": "Новосибирская область", "population": 1625631, "sort_order": 98},
        {"name": "Омск", "region": "Омская область", "population": 1172077, "sort_order": 97},
        {"name": "Красноярск", "region": "Красноярский край", "population": 1093861, "sort_order": 96},
        {"name": "Барнаул", "region": "Алтайский край", "population": 632372, "sort_order": 85},
        {"name": "Иркутск", "region": "Иркутская область", "population": 617264, "sort_order": 84},
        {"name": "Кемерово", "region": "Кемеровская область", "population": 552546, "sort_order": 83},
        {"name": "Томск", "region": "Томская область", "population": 572740, "sort_order": 82},
        {"name": "Новокузнецк", "region": "Кемеровская область", "population": 537480, "sort_order": 81},
        {"name": "Улан-Удэ", "region": "Республика Бурятия", "population": 437565, "sort_order": 80},
        {"name": "Чита", "region": "Забайкальский край", "population": 350861, "sort_order": 79},
        {"name": "Абакан", "region": "Республика Хакасия", "population": 184769, "sort_order": 78},
        {"name": "Кызыл", "region": "Республика Тыва", "population": 125241, "sort_order": 77},
        
        # Дальневосточный федеральный округ
        {"name": "Владивосток", "region": "Приморский край", "population": 600378, "sort_order": 85},
        {"name": "Хабаровск", "region": "Хабаровский край", "population": 617441, "sort_order": 84},
        {"name": "Якутск", "region": "Республика Саха (Якутия)", "population": 322987, "sort_order": 83},
        {"name": "Комсомольск-на-Амуре", "region": "Хабаровский край", "population": 238505, "sort_order": 82},
        {"name": "Благовещенск", "region": "Амурская область", "population": 241437, "sort_order": 81},
        {"name": "Петропавловск-Камчатский", "region": "Камчатский край", "population": 179586, "sort_order": 80},
        {"name": "Южно-Сахалинск", "region": "Сахалинская область", "population": 200636, "sort_order": 79},
        {"name": "Магадан", "region": "Магаданская область", "population": 91825, "sort_order": 78},
        {"name": "Анадырь", "region": "Чукотский автономный округ", "population": 15749, "sort_order": 77},
        
        # Северо-Западный федеральный округ
        {"name": "Калининград", "region": "Калининградская область", "population": 475056, "sort_order": 83},
        {"name": "Мурманск", "region": "Мурманская область", "population": 282851, "sort_order": 82},
        {"name": "Петрозаводск", "region": "Республика Карелия", "population": 278551, "sort_order": 81},
        {"name": "Сыктывкар", "region": "Республика Коми", "population": 245083, "sort_order": 80},
        {"name": "Великий Новгород", "region": "Новгородская область", "population": 224286, "sort_order": 79},
        {"name": "Псков", "region": "Псковская область", "population": 209840, "sort_order": 78},
        {"name": "Вологда", "region": "Вологодская область", "population": 313944, "sort_order": 77},
        {"name": "Череповец", "region": "Вологодская область", "population": 305185, "sort_order": 76},
        
        # Северо-Кавказский федеральный округ
        {"name": "Ставрополь", "region": "Ставропольский край", "population": 450680, "sort_order": 85},
        {"name": "Грозный", "region": "Чеченская Республика", "population": 324602, "sort_order": 84},
        {"name": "Махачкала", "region": "Республика Дагестан", "population": 604266, "sort_order": 83},
        {"name": "Владикавказ", "region": "Республика Северная Осетия", "population": 295830, "sort_order": 82},
        {"name": "Нальчик", "region": "Кабардино-Балкарская Республика", "population": 239040, "sort_order": 81},
        {"name": "Черкесск", "region": "Карачаево-Черкесская Республика", "population": 122395, "sort_order": 80},
        {"name": "Магас", "region": "Республика Ингушетия", "population": 15216, "sort_order": 79},
    ]
    
    print("Начинаем инициализацию городов...")
    
    # Создаем приложение
    app = create_app()
    
    with app.app_context():
        db.create_all()  # Создаём все таблицы, если их нет
        # Проверяем, есть ли уже города в базе
        existing_cities = City.query.count()
        if existing_cities > 0:
            print(f"В базе уже есть {existing_cities} городов. Пропускаем инициализацию.")
            return
        
        # Добавляем города
        for city_data in cities_data:
            # Проверяем, существует ли город с таким именем
            existing_city = City.query.filter_by(name=city_data['name']).first()
            if existing_city:
                print(f"Город {city_data['name']} уже существует, пропускаем")
                continue
            
            city = City(**city_data)
            db.session.add(city)
            print(f"Добавлен город: {city_data['name']}")
        
        # Сохраняем изменения
        db.session.commit()
        
        print(f"Успешно добавлено {len(cities_data)} городов!")
        
        # Показываем топ-10 городов
        popular_cities = City.get_popular_cities(10)
        print("\nТоп-10 популярных городов:")
        for i, city in enumerate(popular_cities, 1):
            print(f"{i}. {city.name} ({city.region}) - {city.population:,} чел.")

if __name__ == "__main__":
    init_cities() 