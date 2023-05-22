# Проект Foodgram ("Продуктовый помощник")
![workflow bagde](https://github.com/3gr1v750v/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

![foodgram_main_page_screenshot](https://github.com/3gr1v750v/foodgram-project-react/assets/110385345/64352295-3d16-4051-a89e-7732f724d09d)

## Описание проекта
Приложение Foodgram ("Продуктовый помощник"): сайт, на котором пользователи 
могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться
на публикации других авторов. Сервис "Список покупок" позворяет пользователям 
создавать список продуктов, которые нужно купить для приготовления выбранных 
блюд. 
Бекэнд разработан согласно документации API.
Фронтэнд предоставлен Яндекс.Практикум.

### Структура проекта
- frontend - файлы, необходимые для сборки фронтенда приложения;
- infra — инфраструктура проекта: конфигурационный файл nginx и docker-compose.yml;
- backend - файлы, необходимые для сборки бэкенд приложения;
- data подготовлен список ингредиентов с единицами измерения. Экспорт ингредиентов осуществляется командой `python manage.py importjson`

### Технологии
- Python 3.10
- Django 4.2.1
- Django Rest Framework 3.14.0
- Djoser 2.2
- PostgreSQL

### Возможности проекта
Что могут делать неавторизованные пользователи:
- Создать аккаунт;
- Просматривать рецепты на главной;
- Просматривать отдельные страницы рецептов;
- Фильтровать рецепты по тегам;

Что могут делать авторизованные пользователи:
- Входить в систему под своим логином и паролем;
- Выходить из системы (разлогиниваться);
- Менять свой пароль;
- Создавать/редактировать/удалять собственные рецепты;
- Просматривать рецепты на главной;
- Просматривать страницы пользователей;
- Просматривать отдельные страницы рецептов;
- Фильтровать рецепты по тегам;
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов;
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок;
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок;

Что могут делать администраторы:
- Администратор обладает всеми правами авторизованного пользователя;
- (панель администратора) Изменять пароль любого пользователя;
- (панель администратора) создавать/блокировать/удалять аккаунты пользователей;
- (панель администратора) редактировать/удалять любые рецепты;
- (панель администратора) добавлять/удалять/редактировать ингредиенты;
- (панель администратора) добавлять/удалять/редактировать теги;

## Описание API

### Ресурсы проекта

- Ресурс `auth`: аутентификация;
- Ресурс `users`: пользователи;
- Ресурс `tags`: теги рецептов ("Завтрак", "Обед");
- Ресурс `recipes`: описание рецептов; 
- Ресурс `ingredients`: ингредиенты, входящие в состав рецептов;

### Документация
Подробное описание ресурсов доступно в документации после запуска проекта по адресу `http://localhost/api/docs/`.

В документации указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры (паджинация, поиск, фильтрация итд.), когда это необходимо.

### Примеры запросов

- Просмотр списока пользователей
```
GET /api/users/?page=<integer>&limit=<integer>
```
- Регистрация пользователя
```
POST /api/users/
```
- Получение токена авторизации
```
POST /api/auth/token/login/
```
Пример JSON body:
```
{
    "password": "Qwerty123",
    "email": "user@host.ru"
}
```
- Изменение пароля
```
POST /api/users/set_password/
```
- Изменение данных пользователя (своих):
```
POST/PATCH /api/users/me/
```
- Просмотр тегов
```
GET /api/tags/
```
- Просмотр списка рецептов
```
GET /api/recipes/
```
Пример ответа:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "Завтрак",
                    "color": "#49B64E",
                    "slug": "zavtrak"
                }
            ],
            "author": {
                "email": "vpupkin@yandex.ru",
                "id": 3,
                "username": "vasia.pupkin",
                "first_name": "Вася",
                "last_name": "Пупкин",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 2,
                    "name": "ячмень",
                    "measurement_unit": "г",
                    "amount": 100
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Рецепт от Васи",
            "image": "http://127.0.0.1:8000/media/recipes/images/%D0%9A%D0%BE%D0%BD%D0%B4%D0%B8%D1%86%D0%B8%D0%BE%D0%BD%D0%B5%D1%80_%D0%B2_%D0%9C%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE.PNG",
            "text": "Описание рецепта",
            "cooking_time": 10
        }
    ]
}
```
- Создание / Изменение собственного рецепта и удаление рецепта
```
POST/PATCH/DELETE /api/recipes
```
Пример JSON body:
```
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
    "tags": [
        1
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
- Добавление в список покупок и удаление из списка
```
POST/DELETE /api/recipes/5/shopping_cart/
```
- Добавление в список избранного и удаление из списка
```
POST/DELETE /api/recipes/5/favorite/
```
- Просмотр списка подписок на авторов
```
GET /api/users/subscriptions/
```
- Просмотр списка подписок на авторов
```
GET /api/users/subscriptions/
```
- Подписка на автора и снятие подписки
```
POST/DELETE /api/users/3/subscribe/ 
```
- Просмотр списка доступных ингредиентов
```
GET /api/ingredients/
```

## Локальный запуск проекта (backend в режиме отладки)
1. Скопируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/3gr1v750v/foodgram-project-react
```

```
cd foodgram-project-react
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3. Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Создайте фаил .env в директории проекта 'infra':
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
5. Примените следующие настройки для 'docker-compose.yml':
```
version: '3.3'
services:
  db:
    image: postgres:14-alpine
    env_file:
      - .env
    ports:
      - 5432:5432 # открываем порты наружу
    volumes:
      - db_data:/var/lib/postgresql/data/
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    volumes:
      - ../frontend/:/app/result_build/
  nginx:
    image: nginx:1.19.3
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ../frontend/build:/usr/share/nginx/html/
      - ../docs/:/usr/share/nginx/html/api/docs/
volumes:
  db_data:
```
6. Примените следующие настройки для 'nginx.conf':
```
server {
    listen 80;
    location /api/ {
        proxy_pass http://host.docker.internal:8000;
    }
    location /admin/ {
        proxy_pass http://host.docker.internal:8000/admin/;
    }
    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.html $uri/swagger.html;
    }
    location / {
        root /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri /index.html;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
      }
      error_page   500 502 503 504  /50x.html;
      location = /50x.html {
        root   /var/html/frontend/;
      }
}
```
7. Перейдите в папку 'infra' и выполните команду сборки контейнеров:
```
cd infra/
```
```
docker compose up
```
Теперь вы можете посмотреть документацию API по адресу `http://localhost/api/docs/redoc.html`

8. Осуществите подключение к базе данных PostgreSQL:

Вы можете подключиться к PostgreSQL удобным для вас способом, например через
меню 'Database' в Pycharm.


9. Выполните миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
10. Создайте учетную запись администратора:
```
python manage.py createsuperuser
```

11. Загрузите тестовые данные:

```
python manage.py importjson
```

12. Запустите бекэнд сервер:

```
python manage.py runserver
```

13. Откройте вебсайт в браузере и можете начинать работу с сайтом:
```
http://localhost/signin
```
## Локальный запуск проекта (Docker Compose)
1. Скопируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/3gr1v750v/foodgram-project-react
```

```
cd foodgram-project-react
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3. Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Создайте фаил .env в директории проекта 'infra':
```
SECRET_KEY = 'secret key used in production'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
5. Измените адрес локального сервера в nginx.conf
```
    server_name 127.0.0.1;
```
6. Перейдите в папку 'infra' и выполните команду сборки контейнеров:
```
cd infra/
```
```
docker compose up -d
```
7. Выполните миграции, создайте суперпользователя и соберите статику:
```
docker compose exec backend python manage.py makemigrations
```
```
docker compose exec backend python manage.py migrate
```
```
docker compose exec backend python manage.py createsuperuser
```
```
docker compose exec backend python manage.py collectstatic --no-input
```

Теперь вы можете зайти на сайт:
- Документация API: http://localhost/api/docs/redoc.html
- Панель администратора: http://localhost/admin/
- Главная страница сайта: http://localhost/recipes

8. Выполните миграцию базы данных Ingredients:
- Скопируйте папку ```data``` в контейнер ```backend```
```
cd foodgram-project-react
```
```
docker cp data/ <container_id>:data/
```
- Выполните команду миграции данных:
```
docker compose exec backend python manage.py importjson
```
В консоли IDE вы должны получить сообщение об успешной миграции данных.

## Разворачивание проекта на сервере (Docker Compose)

### Настройка VM (Ubuntu 22.04) для Docker Compose V2:
Документация: https://docs.docker.com/compose/install/linux/

- Остановите работу nginx, если он у вас установлен и запущен

```sudo systemctl stop nginx```

- Установите последние обновления на виртуальную машину

```sudo apt update```

```sudo apt upgrade -y```

- Установите Docker

```sudo apt install docker.io```

- Установите Docker Compose V2

```sudo mkdir -p /usr/local/lib/docker/cli-plugins```

```sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose```

```sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose```

### Подготовка для запуска проекта на VM:
- Укажите публичный адрес вашего сервера в nginx/default.conf

```server_name <ip вашего сервера>;```

- Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно. Если вы копируете файлы этого проекта, не забудьте поменять конфигурацию параметра 'image' в docker-compose.yaml.

```scp my_file username@host:<путь-на-сервере>```

например

```scp docker-compose.yml <username>@public_ip:/home/<username>/```

### Подготовка "Actions secrets and variables":
- В разделе 'Settings' вашего репозитория, пройдите в раздел 'Secrets and Variables' - 'Actions' и создайте следующие 'repository secrets'

SSH_KEY можно получить командой ````'cat ~/.ssh/id_rsa'```` на машине у которой есть доступ к серверу. Необходимо скопировать всё, включая начало и конец ответа
```
DOCKER_PASSWORD = <dockerhub password>
DOCKER_USERNAME = <dockerhub username>
HOST = <VM public IP>
USER = <VM login>
PASSPHRASE = <VM password>
SECRET_KEY = <Django secret key>
SSH_KEY = <SSH key of the machine that has access to VM>
DB_ENGINE = django.db.backends.postgresql
DB_NAME = <database name>
POSTGRES_USER = <user name>
POSTGRES_PASSWORD = <password>
DB_HOST = <data base host> eg: db
DB_PORT = <database port> eg: 5432
```

### Работа с контейнерами на сервере
1. Зайдите на ваш сервер 
```ssh your_login@public_ip```

2. Если вы скопировали файлы настрек docker в главную директорию, то можете сразу применять 
команды, в противном случае, пройдите к директорию, где у вас находится фаил docker-compose.yml
```
docker compose exec backend python manage.py makemigrations
```
```
docker compose exec backend python manage.py migrate
```
```
docker compose exec backend python manage.py createsuperuser
```
```
docker compose exec backend python manage.py collectstatic --no-input
```

3. Осуществите миграцию данных таблицы "Ингредиенты" на сервере.

а. Скопируйте папку ```data``` на ваш сервер
```
scp -r имя_папки username@public_id:/home/username/
```
b. Найдите id контейнера backend
```
docker container ls
```
c. Скопируйте папку ```data``` в контейнер
```
docker cp data/ <container_id>:data/
```
d. Импортируйте данные
```
docker compose exec backend python manage.py importjson
```

4. Добавьте API документацию:

а. Скопируйте папку ```docs``` на ваш сервер
```
scp -r имя_папки username@public_id:/home/username/
```
b. Найдите id контейнера nginx
```
docker container ls
```
c. Скопируйте данные из папки ```docs``` в контейнер nginx
```
docker cp docs/. <container_id>:/usr/share/nginx/html/api/docs

```
d. Проверьте, что данные скопировались корректно
```
sudo docker exec <container_name> ls /usr/share/nginx/html/api/docs
```

### Github Actions CI:

Запуск workflow осуществляется тригером 'push' в любую ветку репозитория:
- Проверка lint по PEP8
- Создание образа докера (Image) для ./backend
- Создание образа докера (Image) для ./frontend
- Сохранение образов докера (Image) в репозитории docker hub
- Подключение к серверу (виртуальная машина на ubuntu 22.04)
- Остановка работы текущих контейнеров на сервере, очищение временных образов
- Загрузка нового образа на сервер из репозитория docker hub
- Настройка .env файла на сервере
- Разворачивание контейнеров на сервере

Теперь вы можете зайти на сайт (адрес сервера дан для примера):
- Документация API: http://158.160.35.211/api/docs/redoc.html
- Панель администратора: http://158.160.35.211/admin
- Главная страница сайта: http://158.160.35.211/recipes

