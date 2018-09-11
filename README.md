# CS2102-Project
AY2018/2019 Sem 1 - CS2102 Project
This is based on topic C, Stuff Sharing.

## Installing dependencies
`pip install -r requirements.txt`

## Setting up postgresql
1. Setup postgresql from the [official documentation](https://www.postgresql.org/docs/10/static/index.html) under chapter 16
1. Setup your `.pgpass` file for secure storage of password and port as explained [here](https://www.postgresql.org/docs/9.3/static/libpq-pgpass.html) or [this SO post for linux/mac](https://stackoverflow.com/questions/28800880/python-connect-to-postgresql-with-libpq-pgpass) 
1. Replace the dbname and user values in db/__init__.py

## Running the app
1. Clone the repo
1. Install the dependencies
1. Setup the database configurations for postgresql
1. The required configurations have been set in `.flaskenv` so run the app using `flask run`
