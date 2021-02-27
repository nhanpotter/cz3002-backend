# cz3002-backend
default Swagger API document address: root address: eg http://localhost:8000
# install guide
## install dependency
You can use pip to install all package yourself, the dependency list in pipfile, just ignore below
```
// install pipenv
$ pip install pipenv

//install dependency
$ pipenv install
```
## database migration
```
$ python manage.py makemigrations
$ python manage.py migrate
```

## run server
```
//to start environement in console
$ pipenv shell

// run server
python manage.py runserver

//with port
python manage.py runserver 8080
```
# for email you can change email addr and pasword in settings, or use .env below 
1. create a .env file under cz_3002_backend, not the folder contain pipfile
2. add 2 line in it
    * export EMAIL_HOST_USER=your_emal
    * export EMAIL_HOST_PASSWORD=password
    //in terminal
//in terminal
```
$ source .env
```