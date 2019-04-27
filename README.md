# Flask Boilerplate 4Geeks Academy

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io#https://github.com/4GeeksAcademy/flask-rest-hello.git)

1. Make sure you have python 3.6+
```sh
pipenv shell
pipenv install
```

2. Run the migrations
```sh
$ flask db upgrade
```

3. Run flask
```
$ flask run -p 3000
```

## What to do next?

There is an example API working with an database.

## Migrate every time you change your models

You have to generate the migrations for every update your make to your models:
```
$ flask db migrate
```
