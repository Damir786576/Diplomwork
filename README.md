# Document Search Project

## Описание
Простой поисковик по текстам документов с использованием Django, PostgreSQL и Elasticsearch.

## Установка
1. Установите Docker Compose.

## Структура проекта
- `documents/`: Модель Document, сериализаторы, представления, URL и тесты.
- `document_search/`: Основные настройки Django.
- `docker-compose.yml`: Конфигурация Docker.
- `Dockerfile`: Настройки сборки контейнера.

## Команды для запуска
- `docker-compose up --build` - запускает проект.
- `docker-compose exec web python manage.py test` - запускает тесты.
- `http://127.0.0.1:8000/api/documents/` - сайт.