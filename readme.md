Team Finder

Описание
Платформа для поиска команды и управления проектами. Позволяет создавать профили, указывать навыки, публиковать проекты и присоединяться к разработке.

Требования
Docker
Docker Compose

Запуск

1. Создайте файл .env в корне проекта со следующим содержимым:
DJANGO_SECRET_KEY=django-insecure-change-me
DEBUG=True
POSTGRES_DB=teamfinder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

2. Запустите контейнеры:
docker compose up --build -d

3. Примените миграции:
docker compose exec web python manage.py migrate

4. Загрузите тестовые данные:
docker compose exec web python manage.py loaddata fixtures/skills.json fixtures/users.json fixtures/projects.json fixtures/user_skills.json

5. Установите пароли для тестовых аккаунтов:
docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); [u.set_password('password123') or u.save() for u in User.objects.filter(email__in=['alice@test.com', 'bob@test.com', 'carol@test.com'])]"

Тестовые аккаунты
alice@test.com / password123
bob@test.com / password123
carol@test.com / password123

Администрирование
Панель управления: /admin/
Создание администратора:
docker compose exec web python manage.py createsuperuser

Структура проекта
users/ — профили, навыки, аутентификация
projects/ — проекты, участники, статусы
fixtures/ — тестовые данные
templates/ — HTML-шаблоны
static/ — CSS, JS, изображения
docker-compose.yml — конфигурация контейнеров
Dockerfile — образ приложения