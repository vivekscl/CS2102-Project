# CS2102-Project
AY2018/2019 Sem 1 - CS2102 Project
This is based on topic C, Stuff Sharing.

## Installing dependencies
`pip install -r requirements.txt`

## Setting up postgresql
1. Setup postgresql from the [official documentation](https://www.postgresql.org/docs/10/static/index.html) under chapter 16/17
1. Setup your `.pgpass` file for secure storage of password and port as explained [here](https://www.postgresql.org/docs/9.3/static/libpq-pgpass.html) or [this SO post for linux/mac](https://stackoverflow.com/questions/28800880/python-connect-to-postgresql-with-libpq-pgpass) 
1. Replace the dbname and username values for db/__init__.py in [line 24](https://github.com/vivekscl/CS2102-Project/blob/master/db/__init__.py#L24) and the username value in [line 32](https://github.com/vivekscl/CS2102-Project/blob/master/db/__init__.py#L32)

## Running the app
1. Clone the repo
1. [Install the dependencies](#Installing-dependencies)
1. [Setup the database configurations for postgresql](#Setting-up-postgresql)
1. The required configurations have been set in `.flaskenv` so run the app using `flask run`
