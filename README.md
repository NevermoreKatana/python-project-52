# Проект "Менеджер задач"

## Описание
Task Manager – система управления задачами, подобная http://www.redmine.org/. Она позволяет ставить задачи, назначать исполнителей и менять их статусы. Для работы с системой требуется регистрация и аутентификация:

## Установка 

```sh
make install
```

## Запуск сервера(ASGI make)
```sh
make start-dev
```
## Запуск сервера(ASGI docker контейнера)
```sh
make docker-build
```
## Запуск сервера(WSGI make)
```sh
make start-production
```
## Генерация секретного ключа джанго(WSGI make)
```sh
make secretkey
```
## Заполнение .env
```
SECRET_KEY=Секретный ключ джанго
DB_URL=Ссылка на БД пример для Postgre(postgres://USER:PASSWORD@HOST:PORT/NAME)
DEBUG=True/False
TOKEN=Токен для Rollbar
```
### Hexlet tests and linter status:
[![Actions Status](https://github.com/NevermoreKatana/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/NevermoreKatana/python-project-52/actions)

## Результат можно посмотреть

[Task manager](https://task-manager-qvjg.onrender.com/)





