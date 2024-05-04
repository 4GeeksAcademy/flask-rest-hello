import math, os, signal, subprocess
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# this only runs if `$ python remake.py` is executed
if __name__ == '__main__':
    __LOG__= open("refresh.log","w")
    __PBS__= 78

    def __clamp(n): return 0 if n < 0 else __PBS__ if n > __PBS__ else n
    def __run(cmd): subprocess.run(cmd.split(" "), stdout= __LOG__, stderr= __LOG__) # capture their log into refresh.log
    def __print(n, line):
        pbc= __clamp(math.floor(__PBS__ * n))
        pbl= __PBS__ - pbc
        bar= f"|\033[42m{' '*pbc}\033[0;53;4;40;30m{' '*pbl}\033[0m|"
        text = f"{bar}\n    \033[6m{line}\033[0m{' '*(76-len(line))}"
        if n < 1.0: text+= "\033[F"*2
        print(text)

    print("")
    __print(0.00, "Wipping DB")
    __run("flask --app remake run")

    __print(0.15, "Removing current migrations")
    __run("rm -rf migrations")

    __print(0.18, "Recreating migrations")
    __run("flask db init")

    __print(0.32, "Setting up DB")
    __run("flask db upgrade")

    __print(0.58, "Creating revision")
    __run("flask db migrate")

    __print(0.87, "Uploading revision")
    __run("flask db upgrade")

    __print(1.0, "Done!")
    print("\033[0m")

else:
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:////tmp/example.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    MIGRATE = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.reflect()
        db.drop_all()
        db.session.commit()
        os.kill(os.getpid(), signal.SIGTERM)