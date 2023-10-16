docker-build:
	docker-compose up --build
install:
	poetry install
start-dev:
	poetry run python manage.py runserver
secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'
start-production:
	poetry run gunicorn -b 0.0.0.0:8000 task_manager.wsgi:application
migrate-u:
	poetry run python manage.py migrate users
make-migrate-u:
	poetry run python manage.py makemigrations users
migrate:
	poetry run python manage.py migrate
make-migrate:
	poetry run python manage.py makemigrations
test:
	poetry run python manage.py test
make lint:
	poetry run flake8 task_manager