# Проект Django REST Framework в Docker Compose

Этот проект представляет собой пример Cooks Corner приложения, запущенного с использованием Docker Compose.

## Установка

1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/RamazanImashov/Neobis-Cooks-Corner.git
    ```

3. Перейдите в каталог проекта:

    ```bash
    cd Neobis-Cooks-Corner
    ```

4. Создайте файл `.env` в корне проекта и определите необходимые переменные окружения. Пример:

    ```plaintext
    SECRET_KEY=your_secret_key
    DEBUG=False
    DB_NAME=cooks_project
    DB_USER=postgres
    DB_PASS=1234
    DB_HOST=cooks-postgres
    RedisHost=redis
    
    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_host_password
    
    CLOUD_NAME=your_cloud_name
    API_KEY=your_cloud_key
    API_SECRET=your_cloud_sercet
    ```

## Запуск

1. Запустите приложение с помощью Docker Compose:

    ```bash
    docker-compose up --build -d
    ```

2. После успешного запуска, приложение будет доступно по адресу `http://localhost:8000/`.

## Эксплуатация

- Для остановки контейнеров используйте команду:

    ```bash
    docker-compose down
    ```

- Для выполнения миграций Django:

    ```bash
    docker-compose exec CooksCorner python manage.py migrate
    ```

- Для создания суперпользователя:

    ```bash
    docker-compose exec CooksCorner python manage.py createsuperuser
    ```

## Дополнительные настройки

- Чтобы изменить порт, на котором работает приложение, отредактируйте `docker-compose.yml`.
- Для настройки других параметров Django, отредактируйте `settings.py` в директории `your_project_name`.

---

Просто замените `your-username` и `your-repository` на ваше имя пользователя и название репозитория. А также замените `your_project_name` на название вашего Django проекта.
