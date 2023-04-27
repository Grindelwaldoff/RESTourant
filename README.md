# RESTourant

### Описание проекта

Данное API было сделано для будущего веб-приложения ресторана в Армении. API разделено на две части: SuperAdmin и Business. В первой реализуется админинстрирование всех существующих бизнесов и пользователей. Во вторую имеет доступ только конкретный бизнес или Главный Админ. В ней реализуется добавление и редактирование меню, а также аккаунтов официантов. В рамках реализации проекта был выполнен деплой Docker контейнере на виртуальную машину.

### Пользовательские роли

1. Superuser - Главный Админ, который может осуществлять администрирование всех данных
2. Business - Бизнес зарегистрированный в системе, имеет доступ только к своему меню, категориям, официантам, столам.
3. Waiter - Модель официанта, создается конкретным бизнесом.

### Описание реализованных функций

Business:

    * Добавление и редактирование блюд
    * Добавление и редактирование категорий для блюд
    * Добавление и редактирование столов
    * Генерация QR-code, содержащих ссылку, ведущюю к определенному столу
    * Добавление и аутентицикация по JWT Официантов

SuperAdmin:

    * Аутентификация по JWT Главных Админов и Бизнесса
    * Добавление и редактирование объектов "бизнес"

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Grindelwaldoff/RESTourant.git
```

Далее необходимо добавить файл переменных окружения с произвольными данными.

```
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
```

Далее запустить контейнер:

```
sudo docker-compose up -d
```

Провести миграции:

```
sudo docker-compose exec web python manage.py makemigrations
```

```
sudo docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
sudo docker-compose exec web python manage.py createsuperuser
```

Сайт откроется по этой ссылке:

```
http://127.0.0.1/admin/
```

#### Используемые технологии:
* Python 3.8
* Django 3.2
* PostgreSQL
* Docker
* JWT-Auth
* NGINX
* Django Rest Framework

### Автор
Grindewaldoff
