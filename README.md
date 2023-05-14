# Проект Foodgram ("Продуктовый помощник")

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

Что могут делать авторизованные пользователи
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

## Локальный запуск проекта (через Docker контейнеры)
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
        proxy_pass http://host.docker.internal:8000; # эта настройка позволяет обращаться по адресу localhost
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

