# This file was created to run the application on Heroku using gunicorn
from app import app

if __name__ == "__main__":
    app.run()
