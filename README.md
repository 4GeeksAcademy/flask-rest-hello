# Flask Boilerplate 4Geeks Academy

1. Make sure you have python 3.6+
```sh
pyenv install 3.6.6
pyenv global 3.6.6
sudo pip install pipenv
pip install --upgrade pip
pipenv shell
pipenv install
```

1. Configure thde database
```sh
$ export FLASK_APP=app.py

$ flask db init
$ flask db migrate
$ flask db upgrade

```

1. Run flask
```
$ flask run -h $IP -p $PORT
```
