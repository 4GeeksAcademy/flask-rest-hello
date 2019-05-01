# Flask Boilerplate 4Geeks Academy

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io#https://github.com/4GeeksAcademy/flask-rest-hello.git)

1. Make sure you have python 3.6+
```sh
pipenv install
```

2. Run the migrations
```sh
$ pipenv run migrate
```

3. Run flask
```
$ pipenv run start
```

## What to do next?

There is an example API working with an database.

## Migrate every time you change your models

You have to upgrade the migrations for every update your make to your models:
```
$ pipenv run migrate
$ pipenv run upgrade
```
