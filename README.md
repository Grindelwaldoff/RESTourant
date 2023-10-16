# RESTourant
##Description of the project
This API was created for a future web application for a restaurant in Armenia. The API is divided into two parts: SuperAdmin and Business. The first part implements the administration of all existing businesses and users. The second part has access only to a specific business or the Main Admin. In it, the menu is added and edited, as well as the accounts of waiters. During the implementation of the project, a Docker container was deployed on a virtual machine.

##User roles
Superuser - Main Admin, who can perform data administration
Business - Business registered in the system, has access only to its menu, categories, waiters, tables.
Waiter - Waiter model, created for a specific business.
Description of implemented functions
###Business:

* Adding and editing dishes
* Adding and editing categories for dishes
* Adding and editing tables
* Generating QR-code containing a link leading to a specific table
* Adding and authenticating waiters by JWT

###SuperAdmin:

* Authentication by JWT of Main Admins and Businesses
* Adding and editing objects "business"

How to run the project:
Clone the repository and go to it in the command line:

```
git clone https://github.com/Grindelwaldoff/RESTourant.git
```

Next, you need to add a file with environment variables with random data.

```
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
```

Then start the container:

```
sudo docker-compose up -d
```

##Perform migrations:

```
sudo docker-compose exec web python manage.py makemigrations

sudo docker-compose exec web python manage.py migrate
```

Create a superuser:

```
sudo docker-compose exec web python manage.py createsuperuser
```

The site will open at this link:

```
http://127.0.0.1/admin/
```

Used technologies:
* Python 3.8
* Django 3.2
* PostgreSQL
* Docker
* JWT-Auth
* NGINX
* Django Rest Framework
Author
Grindewaldoff
