# Flask Boilerplate for profesional development

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io#https://github.com/4GeeksAcademy/flask-rest-hello.git)

## Features

- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.
- Documented Examples [here](https://github.com/4GeeksAcademy/flask-rest-hello/tree/master/docs).

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


# Manual Instalation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `MySQL` installed on your computer, then run the following commands:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```


## Deploy your website to heroku

This template is 100% compatible with heroku, just make sure to understand and execute the following steps

1. Install heroku
```sh
$ npm i heroku -g
```

2. Login to heroku on the command line
```sh
$ heroku login -i
```
3. Create an application (if you don't have it already)
```sh
$ heroku create <your_application_name>
```
4. Commit and push to heroku
Make sure you have commited your changes and push to heroku
```sh
$ git push heroku master
```
