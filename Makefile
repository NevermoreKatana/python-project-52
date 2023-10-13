docker-build:
	docker build -t postgre .
docker-run-postgre:
	docker run --name postgre --env-file .env -d -p 5432:5432 postgre
install:
	poetry install
start-dev:
	poetry run python manage.py runserver 8000
secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

start-production:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run gunicorn -b 0.0.0.0:8000 task_manager.wsgi:application
