/**
 * Красивый селектор городов с автодополнением
 */
class CitySelector {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.options = {
            placeholder: 'Выберите город...',
            popularLimit: 12,
            searchDelay: 300,
            ...options
        };
        
        this.selectedCity = null;
        this.searchTimeout = null;
        this.isDropdownOpen = false;
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error(`CitySelector: Container with id "${this.containerId}" not found`);
            return;
        }
        
        this.render();
        this.bindEvents();
        this.loadPopularCities();
        
        // Проверяем сохраненный город
        const savedCity = localStorage.getItem('selectedCity');
        if (savedCity) {
            try {
                this.selectedCity = JSON.parse(savedCity);
                this.updateDisplay();
            } catch (e) {
                console.error('Error parsing saved city:', e);
            }
        }
    }
    
    render() {
        this.container.innerHTML = `
            <div class="city-selector">
                <div class="city-selector__input-wrapper">
                    <input type="text" 
                           class="city-selector__input" 
                           placeholder="${this.options.placeholder}"
                           autocomplete="off">
                    <div class="city-selector__icon">🌍</div>
                </div>
                <div class="city-selector__dropdown" style="display: none;">
                    <div class="city-selector__popular">
                        <h4>Популярные города</h4>
                        <div class="city-selector__popular-list"></div>
                    </div>
                    <div class="city-selector__search-results"></div>
                </div>
            </div>
        `;
        
        this.input = this.container.querySelector('.city-selector__input');
        this.dropdown = this.container.querySelector('.city-selector__dropdown');
        this.popularList = this.container.querySelector('.city-selector__popular-list');
        this.searchResults = this.container.querySelector('.city-selector__search-results');
    }
    
    bindEvents() {
        // Обработка ввода в поле поиска
        this.input.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            
            if (this.searchTimeout) {
                clearTimeout(this.searchTimeout);
            }
            
            if (query.length >= 2) {
                this.searchTimeout = setTimeout(() => {
                    this.searchCities(query);
                }, this.options.searchDelay);
            } else {
                this.showPopularCities();
            }
        });
        
        // Обработка фокуса
        this.input.addEventListener('focus', () => {
            this.showDropdown();
            this.showPopularCities();
        });
        
        // Обработка клика вне селектора
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.hideDropdown();
            }
        });
        
        // Обработка клавиш
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideDropdown();
            }
        });
    }
    
    async loadPopularCities() {
        try {
            const response = await fetch(`/api/cities/popular?limit=${this.options.popularLimit}`);
            const cities = await response.json();
            
            this.popularCities = cities;
            this.showPopularCities();
        } catch (error) {
            console.error('Error loading popular cities:', error);
        }
    }
    
    showPopularCities() {
        if (!this.popularCities) return;
        
        this.popularList.innerHTML = this.popularCities.map(city => `
            <div class="city-selector__item" data-city-id="${city.id}" data-city-name="${city.name}">
                <span class="city-selector__item-name">${city.name}</span>
                <span class="city-selector__item-region">${city.region}</span>
            </div>
        `).join('');
        
        this.searchResults.innerHTML = '';
        this.bindItemEvents();
    }
    
    async searchCities(query) {
        try {
            const response = await fetch(`/api/cities/search?q=${encodeURIComponent(query)}`);
            const cities = await response.json();
            
            this.searchResults.innerHTML = cities.map(city => `
                <div class="city-selector__item" data-city-id="${city.id}" data-city-name="${city.name}">
                    <span class="city-selector__item-name">${city.name}</span>
                    <span class="city-selector__item-region">${city.region}</span>
                </div>
            `).join('');
            
            this.popularList.innerHTML = '';
            this.bindItemEvents();
        } catch (error) {
            console.error('Error searching cities:', error);
        }
    }
    
    bindItemEvents() {
        const items = this.container.querySelectorAll('.city-selector__item');
        items.forEach(item => {
            item.addEventListener('click', () => {
                const cityId = item.dataset.cityId;
                const cityName = item.dataset.cityName;
                
                this.selectCity({
                    id: parseInt(cityId),
                    name: cityName
                });
                
                this.hideDropdown();
            });
        });
    }
    
    selectCity(city) {
        this.selectedCity = city;
        this.updateDisplay();
        
        // Сохраняем в localStorage
        localStorage.setItem('selectedCity', JSON.stringify(city));
        
        // Вызываем событие
        this.container.dispatchEvent(new CustomEvent('citySelected', {
            detail: { city }
        }));
        
        // Если это модальное окно, активируем кнопку подтверждения
        if (this.containerId === 'modal-city-selector') {
            const confirmBtn = document.getElementById('confirm-city-selection');
            if (confirmBtn) {
                confirmBtn.disabled = false;
            }
        }
    }
    
    updateDisplay() {
        if (this.selectedCity) {
            this.input.value = this.selectedCity.name;
            this.input.classList.add('has-value');
        } else {
            this.input.value = '';
            this.input.classList.remove('has-value');
        }
    }
    
    showDropdown() {
        this.dropdown.style.display = 'block';
        this.isDropdownOpen = true;
    }
    
    hideDropdown() {
        this.dropdown.style.display = 'none';
        this.isDropdownOpen = false;
    }
    
    getSelectedCity() {
        return this.selectedCity;
    }
}

// Инициализация селекторов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализируем селектор в модальном окне
    const modalSelector = new CitySelector('modal-city-selector', {
        placeholder: 'Начните вводить название города...'
    });
    
    // Проверяем, нужно ли показать модальное окно
    const hasSeenCityModal = localStorage.getItem('hasSeenCityModal');
    const selectedCity = localStorage.getItem('selectedCity');
    
    if (!hasSeenCityModal && !selectedCity) {
        setTimeout(() => {
            showCityModal();
        }, 1000); // Показываем через 1 секунду после загрузки
    }
    
    // Обработчики для модального окна
    const cityModal = document.getElementById('city-modal');
    const skipBtn = document.getElementById('skip-city-selection');
    const confirmBtn = document.getElementById('confirm-city-selection');
    
    // Закрытие модального окна кликом вне его области
    if (cityModal) {
        cityModal.addEventListener('click', (e) => {
            if (e.target === cityModal) {
                hideCityModal();
                localStorage.setItem('hasSeenCityModal', 'true');
            }
        });
    }
    
    if (skipBtn) {
        skipBtn.addEventListener('click', () => {
            hideCityModal();
            localStorage.setItem('hasSeenCityModal', 'true');
        });
    }
    
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            const selectedCity = modalSelector.getSelectedCity();
            if (selectedCity) {
                hideCityModal();
                localStorage.setItem('hasSeenCityModal', 'true');
            }
        });
    }
    
    // Обработчик выбора города в модальном окне
    modalSelector.container.addEventListener('citySelected', (e) => {
        const confirmBtn = document.getElementById('confirm-city-selection');
        if (confirmBtn) {
            confirmBtn.disabled = false;
        }
    });
});

function showCityModal() {
    const modal = document.getElementById('city-modal');
    if (modal) {
        modal.classList.add('show');
        // Убираем блокировку прокрутки
        // document.body.style.overflow = 'hidden';
    }
}

function hideCityModal() {
    const modal = document.getElementById('city-modal');
    if (modal) {
        modal.classList.remove('show');
        // Восстанавливаем прокрутку
        // document.body.style.overflow = '';
    }
}

/*
 * City Selector Component
 * Версия: 1.7
 * Обновлено: Убран селектор городов из шапки, оставлено только модальное окно
 */ 