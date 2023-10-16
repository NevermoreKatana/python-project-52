docker-build:
	docker-compose up --build

install:
	poetry install

start-dev:
	poetry run python manage.py runserver

secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

start-production:
	poetry run python manage.py migrate
	poetry run gunicorn -b 0.0.0.0:8000 task_manager.wsgi:application

test:
	poetry run python manage.py test

make lint:
	poetry run flake8 task_manager