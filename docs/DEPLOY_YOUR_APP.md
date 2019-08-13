# Deploying to Heroku

This template is 100% compatible with heroku, just make sure to understand and execute the following steps

1. Install heroku (if you don't have it yet)
```sh
$ npm i heroku -g
```

2. Login to heroku on the command line (if you have not already)
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

## Enviroment Variables

You cannot create a `.env` file on Heroku, instead you need to manually create all the variables under your project settings.

![Configuring Env Variables](https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/assets/env_variables.gif?raw=true)


## Deploying your database to Heroku

You local MySQL Database now has to be uploaded to a cloud, there are plenty of services that provide MySQL database hosting but we recomend JawDB because it has a Free Tier, its simple and 100% integrated with Heroku.

1. Go to your heroku project dashboard and look to add a new heroku add-on.
2. Look for JawDB MySQL and add it to your project (it may ask for a Credit Card but you will not be charged as long as your remain withing 5mb database size, enough for your demo.
3. Once JawDB is added to your project look for the Connection String inside your JawDB dashboard, something like:
```
mysql://tqqa0ui0cga32nxd:eqi8nchjbpwth82v@c584md9egjnm02sk.5btxwkvyhwsf.us-east-1.rds.amazonaws.com:3306/45fds423rbtbr
```
4. Copy the connection string and create a new environment variable on your project settings.

![Create DB on heroku](https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/assets/db_config.gif?raw=true)
