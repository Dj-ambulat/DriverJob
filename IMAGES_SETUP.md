# Инструкция по добавлению изображений на сайт Road Fighters

## Структура папок для изображений

```
static/
├── images/
│   ├── content/          # Основные изображения контента
│   │   ├── hero-truck.jpg
│   │   ├── truck-work.jpg
│   │   └── no-vacancies.jpg
│   ├── icons/            # Иконки (SVG и PNG)
│   │   ├── driver-icon.svg
│   │   ├── employer-icon.svg
│   │   ├── vacancy-icon.svg
│   │   ├── resume-icon.svg
│   │   ├── company-icon.svg
│   │   ├── search-icon.svg
│   │   ├── location-icon.svg
│   │   ├── experience-icon.svg
│   │   └── direction-icon.svg
│   ├── backgrounds/      # Фоновые изображения
│   └── avatars/          # Аватары пользователей
```

## Как добавить изображения

### 1. Основные изображения контента

**Размещение:** `static/images/content/`

**Рекомендуемые размеры:**
- Hero изображения: 800x600px или 1200x800px
- Карточки вакансий: 400x300px
- Общие изображения: 600x400px

**Форматы:** JPG, PNG, WebP

**Примеры:**
- `hero-truck.jpg` - главное изображение на главной странице
- `truck-work.jpg` - изображения для карточек вакансий
- `no-vacancies.jpg` - изображение когда нет вакансий

### 2. Иконки

**Размещение:** `static/images/icons/`

**Рекомендации:**
- Используйте SVG для лучшего качества
- Размер: 100x100px viewBox
- Цвета должны соответствовать дизайну сайта

**Основные цвета сайта:**
- Основной синий: `#2b67f6`
- Акцентный оранжевый: `#f0a500`
- Зеленый: `#4CAF50`
- Белый: `#ffffff`

### 3. Как добавить изображение в шаблон

#### В HTML шаблоне:

```html
<!-- Обычное изображение -->
<img src="{{ url_for('static', filename='images/content/your-image.jpg') }}" 
     alt="Описание изображения" 
     class="your-css-class">

<!-- Иконка -->
<img src="{{ url_for('static', filename='images/icons/your-icon.svg') }}" 
     alt="Описание иконки" 
     style="width: 24px; height: 24px;">
```

#### В CSS:

```css
.your-css-class {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease;
}

.your-css-class:hover {
    transform: scale(1.05);
}
```

## Готовые изображения для сайта

### Созданные SVG иконки:

1. **driver-icon.svg** - иконка водителя
2. **employer-icon.svg** - иконка работодателя
3. **vacancy-icon.svg** - иконка вакансии
4. **resume-icon.svg** - иконка резюме
5. **company-icon.svg** - иконка компании
6. **search-icon.svg** - иконка поиска
7. **location-icon.svg** - иконка местоположения
8. **experience-icon.svg** - иконка опыта
9. **direction-icon.svg** - иконка направления

### Необходимые изображения контента:

Для полной функциональности сайта вам нужно добавить:

1. **hero-truck.jpg** - главное изображение грузовика
2. **truck-work.jpg** - изображение работы водителем
3. **no-vacancies.jpg** - изображение для пустого состояния

## Где найти изображения

### Бесплатные источники:

1. **Unsplash** (unsplash.com) - высококачественные фото
2. **Pexels** (pexels.com) - бесплатные стоковые фото
3. **Pixabay** (pixabay.com) - изображения и иллюстрации
4. **Flaticon** (flaticon.com) - иконки (требуют атрибуции)

### Поисковые запросы для изображений:

- "truck driver work"
- "logistics transportation"
- "delivery truck"
- "professional driver"
- "cargo transportation"

## Оптимизация изображений

### Для веб-сайта:

1. **Сжатие:** Используйте WebP или сжатые JPG
2. **Размеры:** Не загружайте изображения больше необходимого
3. **Lazy loading:** Добавьте `loading="lazy"` для изображений ниже fold

### Пример оптимизированного кода:

```html
<img src="{{ url_for('static', filename='images/content/hero-truck.webp') }}" 
     alt="Грузовик на дороге" 
     class="hero-img"
     loading="lazy"
     width="800" 
     height="600">
```

## Добавление изображений на другие страницы

### Страница резюме:

```html
<div class="resume-card">
    <div class="resume-image">
        <img src="{{ url_for('static', filename='images/content/driver-profile.jpg') }}" 
             alt="Профиль водителя">
    </div>
    <div class="resume-content">
        <!-- Содержимое резюме -->
    </div>
</div>
```

### Страница профиля:

```html
<div class="profile-header">
    <div class="profile-avatar">
        <img src="{{ url_for('static', filename='images/avatars/default-avatar.jpg') }}" 
             alt="Аватар пользователя">
    </div>
    <div class="profile-info">
        <!-- Информация профиля -->
    </div>
</div>
```

## Советы по дизайну

1. **Консистентность:** Используйте единый стиль изображений
2. **Качество:** Выбирайте высококачественные изображения
3. **Релевантность:** Изображения должны соответствовать тематике
4. **Размеры:** Оптимизируйте размеры для быстрой загрузки
5. **Альтернативный текст:** Всегда добавляйте alt-атрибуты

## Проверка после добавления

После добавления изображений проверьте:

1. ✅ Изображения отображаются корректно
2. ✅ Размеры подходят для дизайна
3. ✅ Скорость загрузки страницы не пострадала
4. ✅ Изображения адаптивны на мобильных устройствах
5. ✅ Alt-атрибуты заполнены для SEO 