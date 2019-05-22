# Flask Boilerplate 4Geeks Academy

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io#https://github.com/4GeeksAcademy/flask-rest-hello.git)

## How to stat the project?

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's were your endpoints should be coded)
- src/mode.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)

For a more detailed explanation look for the tutorial inside the `docs` folder.

## Remember migrate every time you change your models

You have to migreate and upgrade the migrations for every update your make to your models:
```
$ pipenv run migrate (to make the migrations)
$ pipenv run upgrade  (to update your databse with the migrations)
```


## Instalation for ubuntu

1. Make sure you have python 3.6+
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```