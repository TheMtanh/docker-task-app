# Список задач в Docker

Приложение на Flask и SQLite: добавление, выполнение и удаление задач.

## Запуск

Требуются Docker и Docker Compose.

    docker compose up -d --build

Открыть http://localhost:8088.

## Данные

База SQLite расположена в контейнере по пути /app/data/tasks.db.
Docker-хранилище tasks-data сохраняет данные при пересоздании контейнера.
Зависимости устанавливаются через Dockerfile.

## Остановка

    docker compose down
