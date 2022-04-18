
# API_YAMDB_FINAL ![api_yamdb](https://github.com/gilbey7s/yamdb_final/workflows/api_yamdb/badge.svg)

Описание:

## Проект API_YaMDB - это API социальной сети, она собирает оценки и отзывы пользователей на различные произведения. 
## В данном проекте реазованы практики CI/CD. Реализован workflow следующих задач: 
* после изменений кода в репозитории, производится проверка линтеров на соответствие кода pep8, запускаются тесты.
* собирается образ проекта, и копируется в docker-hub по адресу - https://hub.docker.com/repository/docker/gilbey7s/api_yamdb
* если код был обновлен в ветке master/main проект разворачивается на хосте.
* производится оповещание об успешной работе workflow в бот telegram

##  Адрес проекта http://51.250.82.176/redoc/
### Технологии

* Django,
* djangorestframework,
* djangorestframework_simplejwt,
* postgres,
* ngnix,
* gunicorn,
* docker,
* docker-compose,
* CI/CD


### Развертывание приложений в Docker-контейнерах:
* Клонируем репозиторий на локальную машину;
* Из репозитория копируем в директорию проекта файлы - docker-compose.yaml и каталог nginx/ с файлом default.conf 
* Установливаем на локальную машину Docker - https://www.docker.com/get-started/ и Docker-compose если ОС локальной машины Linux https://docs.docker.com/compose/install/
* Файл для подключения базы данных;
    Создайте файл .env в директории проекта следующего соддержания:
    (Настройки по умолчанию)
    - DB_ENGINE=django.db.backends.postgresql
    - DB_NAME=postgres
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - DB_HOST=db
    - DB_PORT=5432

* Поднимаем контенеры - sudo docker-compose up -d;
* Запускаем миграции - sudo docker-compose exec web python manage.py migrate
* Создаем superuser - sudo docker-compose exec web python manage.py createsuperuser
* Собираем статику - sudo docker-compose exec web python manage.py collectstatic --no-input

### Документация после запуска контейнеров находится по адресу  http://<host>redoc/

### Доступные эндпоинты:

- api/v1/auth/signup/ - Авторизация
- api/v1/auth/token/ - Получение JWT-токена
- api/v1/users/ - Пользователи
- api/v1/users/me/ - Профиль
- api/v1/categories/ -  Категории произведений
- api/v1/genres/ - Жанры произведений
- api/v1/titles/ - Произведения, к которым пишут отзывы
- api/v1/titles/{title_id}/reviews - Oтзывы
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Комментарии к отзывам

## Автор: Чумак Виталий