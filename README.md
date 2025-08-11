# FastAPI Project - Система управления балансами

Проект представляет собой REST API для управления пользователями, аккаунтами и платежами, построенный на FastAPI с использованием PostgreSQL и Alembic для миграций.

## Технологии

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM
- **Alembic** - миграции базы данных
- **Poetry** - управление зависимостями
- **Docker & Docker Compose** - контейнеризация
- **JWT** - аутентификация

## Структура проекта

```
├── app/
│   ├── api/routes/     # API маршруты
│   ├── config/         # Конфигурация
│   ├── database/       # Настройки БД и миграции
│   ├── models/         # Модели данных
│   ├── repositories/   # Репозитории для работы с БД
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   └── utils/          # Утилиты
├── tests/              # Тесты
├── docker-compose.yml  # Docker Compose конфигурация
├── Dockerfile          # Docker образ
├── pyproject.toml      # Poetry конфигурация
└── alembic.ini         # Alembic конфигурация
```

## Запуск проекта

### Вариант 1: С использованием Docker Compose (рекомендуется)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/BahaGit2002/balance_flow
   cd balance_flow
   ```

2. **Запустите проект:**
   ```bash
   docker-compose up --build
   ```

3. **Примените миграции:**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

4. **Создайте первого администратора:**
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
        -H "Content-Type: application/json" \
        -d '{
          "full_name": "Администратор",
          "email": "admin@example.com",
          "password": "admin123"
        }'
   ```

5. **Обновите пользователя до администратора в базе данных:**
   ```bash
   docker-compose exec db psql -U root -d balance_flow_db -c "UPDATE users SET is_admin = true WHERE email = 'admin@example.com';"
   ```

### Вариант 2: Локальный запуск

1. **Установите зависимости:**
   ```bash
   # Установите Poetry (если не установлен)
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Установите зависимости проекта
   poetry install
   ```

2. **Настройте переменные окружения:**
   ```bash
   cp .env_example .env
   ```
   
   Отредактируйте `.env` файл:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql+asyncpg://root:2D*QgVdv8r9V@localhost:5432/balance_flow_db
   ```

3. **Запустите PostgreSQL:**
   ```bash
   # Используя Docker
   docker run -d \
     --name postgres \
     -e POSTGRES_USER=root \
     -e POSTGRES_PASSWORD=2D*QgVdv8r9V \
     -e POSTGRES_DB=balance_flow_db \
     -p 5432:5432 \
     postgres:15
   ```

4. **Примените миграции:**
   ```bash
   poetry run alembic upgrade head
   ```

5. **Запустите приложение:**
   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Создайте первого администратора:**
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
        -H "Content-Type: application/json" \
        -d '{
          "full_name": "Администратор",
          "email": "admin@example.com",
          "password": "admin123"
        }'
   ```

7. **Обновите пользователя до администратора:**
   ```bash
   docker exec -it postgres psql -U root -d balance_flow_db -c "UPDATE users SET is_admin = true WHERE email = 'admin@example.com';"
   ```

## Учетные данные по умолчанию

После создания первого администратора вы можете использовать следующие учетные данные:

### Администратор
- **Email:** admin@example.com
- **Password:** admin123

### Создание обычного пользователя
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "Пользователь",
       "email": "user@example.com",
       "password": "user123"
     }'
```

## API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему

### Пользователи (требует аутентификации)
- `GET /users/me` - Получить информацию о текущем пользователе
- `GET /users/accounts` - Получить аккаунты пользователя
- `POST /users/accounts` - Создать новый аккаунт

### Администратор (требует прав администратора)
- `GET /admin/me` - Информация об администраторе
- `GET /admin/users` - Список всех пользователей
- `POST /admin/users` - Создать пользователя
- `PUT /admin/users/{user_id}` - Обновить пользователя
- `DELETE /admin/users/{user_id}` - Удалить пользователя

### Webhook
- `POST /webhook` - Обработка webhook'ов для платежей

## Документация API

После запуска приложения документация доступна по адресам:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `SECRET_KEY` | Секретный ключ для JWT | - |
| `DATABASE_URL` | URL подключения к БД | - |
| `ALGORITHM` | Алгоритм JWT | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена | 30 |

## Разработка

### Запуск тестов
```bash
poetry run pytest
```

### Создание новой миграции
```bash
poetry run alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
poetry run alembic upgrade head
```

## Остановка проекта

### Docker Compose
```bash
docker-compose down
```

### Локальный запуск
```bash

docker stop postgres
docker rm postgres
```
