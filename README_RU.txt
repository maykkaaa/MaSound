YOUR SOUND — локальный Django музыкальный сервис

УСТАНОВКА (Windows PowerShell):
1. Распакуй архив в папку MaSound.
2. Открой PowerShell в этой папке.
3. Активируй своё окружение: .venv\Scripts\Activate.ps1
4. Установи зависимости: python -m pip install -r requirements.txt
5. Создай миграции: python manage.py makemigrations tracks social playlists
6. Примени их: python manage.py migrate
7. Создай администратора (необязательно): python manage.py createsuperuser
8. Запусти: python manage.py runserver
9. Открой http://127.0.0.1:8000/

Функции: регистрация/вход/выход, загрузка аудио и обложек, поиск по названию/исполнителю/жанру, HTML5-плеер, лайки, комментарии, плейлисты.

Загрузка: войди в аккаунт -> Upload. Поддерживаются MP3, WAV, OGG, M4A.
Для продакшена настрой SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, PostgreSQL и внешнее хранилище медиа. Используй только музыку, на которую у тебя есть права.
