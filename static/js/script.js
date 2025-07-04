// scripts.js

// Управление фоновой музыкой и анимациями
document.addEventListener('DOMContentLoaded', function() {
    const musicBtn = document.getElementById('music-toggle');
    const audio = document.getElementById('background-music');
    
    // Проверяем, есть ли аудио элемент
    if (!audio || !musicBtn) {
        console.log('Аудио элементы не найдены');
        return;
    }
    
    // Проверяем, была ли музыка включена ранее
    const musicWasPlaying = localStorage.getItem('musicPlaying') === 'true';
    
    // Обработчик ошибок загрузки аудио
    audio.addEventListener('error', function(e) {
        console.log('Ошибка загрузки аудио файла:', e);
        console.log('💡 Для включения фоновой музыки добавьте реальные аудио файлы в папку static/audio/');
        console.log('📁 Требуемые файлы: background-music.mp3 и background-music.ogg');
        musicBtn.style.display = 'none'; // Скрываем кнопку если файл не найден
        musicBtn.title = 'Аудио файл недоступен';
    });
    
    // Обработчик успешной загрузки аудио
    audio.addEventListener('loadeddata', function() {
        console.log('Аудио файл загружен успешно');
        musicBtn.style.display = 'block';
        musicBtn.title = 'Включить/выключить музыку';
        
        // Проверяем, что файл не пустой (длительность > 0)
        if (audio.duration > 0) {
            // Автоматически включаем музыку при загрузке сайта
            audio.play().then(() => {
                musicBtn.classList.add('playing');
                localStorage.setItem('musicPlaying', 'true');
                console.log('🎵 Музыка включена автоматически');
            }).catch(error => {
                console.log('Автовоспроизведение заблокировано браузером:', error);
                // Если автовоспроизведение заблокировано, проверяем предыдущее состояние
                if (musicWasPlaying) {
                    musicBtn.classList.add('playing');
                }
            });
        } else {
            console.log('Аудио файл пустой или поврежден');
            console.log('💡 Для включения фоновой музыки добавьте реальные аудио файлы в папку static/audio/');
            console.log('📁 Требуемые файлы: background-music.mp3 и background-music.ogg');
            musicBtn.style.display = 'none';
            musicBtn.title = 'Аудио файл недоступен';
        }
    });
    
    // Обработчик клика по кнопке музыки
    musicBtn.addEventListener('click', function() {
        if (audio.duration <= 0) {
            console.log('Аудио файл недоступен');
            return;
        }
        
        if (audio.paused) {
            audio.play().then(() => {
                musicBtn.classList.add('playing');
                localStorage.setItem('musicPlaying', 'true');
            }).catch(error => {
                console.log('Ошибка воспроизведения:', error);
            });
        } else {
            audio.pause();
            musicBtn.classList.remove('playing');
            localStorage.setItem('musicPlaying', 'false');
        }
    });
    
    // Обработчик изменения громкости
    audio.volume = 0.3; // Устанавливаем громкость на 30%
    
    // Восстанавливаем музыку при переключении вкладок
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && localStorage.getItem('musicPlaying') === 'true' && audio.paused && audio.duration > 0) {
            audio.play().then(() => {
                musicBtn.classList.add('playing');
            }).catch(error => {
                console.log('Ошибка восстановления музыки:', error);
            });
        }
    });

    // Восстанавливаем музыку при загрузке страницы
    if (musicWasPlaying && audio.paused && audio.duration > 0) {
        audio.play().then(() => {
            musicBtn.classList.add('playing');
        }).catch(error => {
            console.log('Ошибка восстановления музыки при загрузке:', error);
        });
    }
});



// Дополнительные функции для управления музыкой
function setMusicVolume(volume) {
    const audio = document.getElementById('background-music');
    if (audio) {
        audio.volume = Math.max(0, Math.min(1, volume)); // Ограничиваем от 0 до 1
    }
}

function toggleMusic() {
    const musicBtn = document.getElementById('music-toggle');
    if (musicBtn) {
        musicBtn.click();
    }
}

// Экспортируем функции для использования в консоли браузера
window.musicControls = {
    setVolume: setMusicVolume,
    toggle: toggleMusic
};
