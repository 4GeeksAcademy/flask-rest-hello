# Flask Boilerplate for Profesional Development

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/from-referrer/)
<p align="center">
    <a href="https://youtu.be/ORxQ-K3BzQA"><img height="200px" src="https://github.com/4GeeksAcademy/flask-rest-hello/blob/main/docs/assets/how-to.png?raw=true?raw=true" /></a>
</p>

## Features

- Extensive documentation [here](https://start.4geeksacademy.com).
- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## Installation (automatic if you are using gitpod)

> Important: The boiplerplate is made for python 3.7 but you can easily change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv install;
mysql -u root -e "CREATE DATABASE example";
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## How to Start coding?

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:

```bash
$ pipenv run migrate #(to make the migrations)
$ pipenv run upgrade  #(to update your databse with the migrations)
```


# Manual Installation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `MySQL` installed on your computer and MySQL is running, then run the following commands:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```


## Publish/Deploy your website!

This boilerplate it's 100% read to deploy with Render.com and Herkou in a matter of minutes. Please read the [official documentation about it](https://start.4geeksacademy.com/deploy).


### Contributors

This template was built as part of the 4Geeks Academy [Coding Bootcamp](https://4geeksacademy.com/us/coding-bootcamp) by [Alejandro Sanchez](https://twitter.com/alesanchezr) and many other contributors. Find out more about our [Full Stack Developer Course](https://4geeksacademy.com/us/coding-bootcamps/part-time-full-stack-developer), and [Data Science Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning).

You can find other templates and resources like this at the [school github page](https://github.com/4geeksacademy/).
