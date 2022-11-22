print("""



WELCOME GEEK! 🐍 + 💻 = 🤓

The server is already running, \033[94mctr + c\033[0m to stop the server if you like

The following commands are available to run your code:

- \033[94m$ pipenv run migrate\033[0m create database migrations (if models.py is edited)
- \033[94m$ pipenv run upgrade\033[0m run database migrations (if pending)
- \033[94m$ pipenv run start\033[0m start flask web server (if not running)
- \033[94m$ pipenv run deploy\033[0m deploy to heroku (if needed) \n\n
""")