# Система выбора городов для сайта Road Fighters

## 🏙️ Что добавлено:

1. **Модель City** - для хранения информации о городах
2. **API для городов** - поиск и получение списка городов
3. **Красивый селектор** - современный интерфейс с автодополнением
4. **Популярные города** - быстрый выбор популярных городов
5. **Поиск по городам** - фильтрация вакансий и резюме

## 📁 Структура файлов:

```
models.py                    # Модель City
routes.py                    # API маршруты для городов
init_cities.py              # Скрипт инициализации городов
static/
├── js/
│   └── city-selector.js    # JavaScript компонент
└── css/
    └── city-selector.css   # Стили селектора
templates/
└── index.html              # Обновленная главная страница
```

## 🚀 Быстрый старт:

### Шаг 1: Инициализация базы данных
```bash
python init_cities.py
```

### Шаг 2: Проверка работы
1. Откройте главную страницу
2. Нажмите на поле "Город"
3. Выберите город из списка

## 🎨 Особенности дизайна:

### Современный интерфейс:
- **Стеклянный эффект** - backdrop-filter: blur()
- **Плавные анимации** - переходы и трансформации
- **Адаптивность** - работает на всех устройствах
- **Динамические цвета** - меняются по времени суток

### Интерактивность:
- **Автодополнение** - поиск при вводе
- **Популярные города** - быстрый выбор
- **Hover эффекты** - визуальная обратная связь
- **Клавиатурная навигация** - Esc для закрытия

## 🔧 API маршруты:

### Получить все города:
```
GET /api/cities
```

### Поиск городов:
```
GET /api/cities/search?q=москва
```

### Популярные города:
```
GET /api/cities/popular?limit=10
```

## 🎯 Использование:

### В HTML:
```html
<div id="city-selector" data-city-selector="city-selector"></div>
```

### В JavaScript:
```javascript
const citySelector = new CitySelector('city-selector', {
    placeholder: 'Выберите город...',
    showPopular: true,
    maxResults: 10
});

// Обработчик выбора
citySelector.container.addEventListener('citySelected', function(e) {
    console.log('Выбран город:', e.detail);
});
```

## 🏗️ Модель City:

```python
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    region = db.Column(db.String(100), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
```

### Методы:
- `get_popular_cities(limit)` - популярные города
- `search_cities(query, limit)` - поиск по названию

## 🎨 CSS классы:

### Основные:
- `.city-selector` - контейнер селектора
- `.city-selector__input-wrapper` - обертка поля ввода
- `.city-selector__dropdown` - выпадающий список
- `.city-selector__item` - элемент списка

### Состояния:
- `.city-selector__input--selected` - выбранный город
- `.city-selector__no-results` - нет результатов
- `.city-selector__popular-cities` - популярные города

## 🔍 Поиск и фильтрация:

### В маршрутах:
```python
@routes_bp.route('/vacancies')
def vacancies():
    city = request.args.get('city')
    if city:
        vacancies = Vacancy.query.filter_by(city=city).all()
    else:
        vacancies = Vacancy.query.all()
    return render_template('vacancies.html', vacancies=vacancies)
```

### В формах:
```html
<input type="hidden" name="city_id" value="">
<input type="text" name="city_name" readonly>
```

## 📱 Адаптивность:

### Мобильные устройства:
- Уменьшенные отступы
- Увеличенные кнопки
- Оптимизированная сетка

### Планшеты:
- Средние размеры элементов
- Горизонтальная раскладка
- Полная функциональность

## 🎯 Кастомизация:

### Изменение стилей:
```css
.city-selector__input-wrapper {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
}
```

### Изменение анимаций:
```css
@keyframes cityDropdownSlide {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

### Добавление новых городов:
```python
# В init_cities.py
cities_data.append({
    "name": "Новый город",
    "region": "Область",
    "population": 100000,
    "sort_order": 50
})
```

## 🔧 Настройка:

### Параметры селектора:
```javascript
const options = {
    placeholder: 'Выберите город...',
    showPopular: true,
    maxResults: 10,
    minQueryLength: 2
};
```

### Локализация:
```javascript
const messages = {
    noResults: 'Город не найден',
    popularTitle: 'Популярные города',
    placeholder: 'Выберите город...'
};
```

## 🚀 Производительность:

### Оптимизации:
- **Debounce поиска** - 300ms задержка
- **Лимит результатов** - максимум 10 городов
- **Кэширование** - популярные города загружаются один раз
- **Ленивая загрузка** - поиск только при необходимости

### Мониторинг:
```javascript
// В консоли браузера
console.log('Время загрузки городов:', performance.now());
console.log('Количество городов:', cities.length);
```

## ✅ Чек-лист настройки:

- [ ] Запущен скрипт `init_cities.py`
- [ ] Добавлены CSS и JS файлы
- [ ] Проверена работа API
- [ ] Тестирование на мобильных устройствах
- [ ] Проверка поиска и фильтрации
- [ ] Настройка адаптивности
- [ ] Оптимизация производительности

## 🎉 Результат:

После настройки ваш сайт будет иметь:
- Красивый селектор городов с автодополнением
- Быстрый поиск по популярным городам
- Фильтрацию вакансий и резюме по городам
- Современный адаптивный дизайн
- Высокую производительность

Система городов сделает поиск работы более точным и удобным! 🚀 