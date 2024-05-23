from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .admin import site
from .database import engine, get_db
from .utils import APIException, bootstrap_app
from .models import Base, User

app = FastAPI()
app = bootstrap_app(app)
site.mount_app(app)

@app.get('/user')
def handle_hello(db: Session = Depends(get_db)):
    users = db.query(User).all()
    # raise APIException("This is an error", status_code=400)
    response_body = {
        "msg": "Hello, this is your GET /user response, check the data property on this payload ",
        "data": [user.serialize() for user in users]
    }

    return response_body

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise APIException("User not found", status_code=404)
    return user.serialize()