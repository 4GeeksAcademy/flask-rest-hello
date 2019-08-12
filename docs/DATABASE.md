# Creating and/or Accessing the MySQL Database

1. Login in into your mysql terminal:
```sh
$ mysql
```
2. Once inside, check if you have the database already created:
```sql
SHOW databases;
```
3. If you don't see the example database create it by typing:
```sql
CREATE DATABASE example;
```
Note: Make sure to update the `DB_CONNECTION_STRING` on the `.env` file with the correct database name.

3. If you your databse is already created get inside of it by typing:
```sql
USE example;
```
4. No you can type any SQL command you like, for example:
```sql
SHOW TABLES;
```
Note: type `exit;` to quit.


# Querying data using Python and SQL Alchemy (SELECT)

Asuming you have a Person object in your models.py file.

```py
# get all the people
people_query = Person.query.all()

# get only the ones named "Joe"
people_query = Person.query.filter_by(name='Joe')

# map the results and your list of people its now inside all_people variable
all_people = list(map(lambda x: x.serialize(), people_query))


# get just one person
user1 = Person.query.get(person_id)
 ```

## Inserting data

Asuming you have a Person object in your models.py file.

```py
user1 = Person(username="my_super_username", email="my_super@email.com")
db.session.add(user1)
db.session.commit()
```

### Updating data

```py
user1 = Person.query.get(person_id)
if user1 is None:
    raise APIException('User not found', status_code=404)

if "username" in body:
    user1.username = body["username"]
if "email" in body:
    user1.email = body["email"]
db.session.commit()
```
 
 ### Delete data
 
 ```py
 user1 = Person.query.get(person_id)
if user1 is None:
    raise APIException('User not found', status_code=404)
db.session.delete(user1)
db.session.commit()
  ```
