# CS2102-Project
AY2018/2019 Sem 1 - CS2102 Project
This is based on topic C, Stuff Sharing.

## Installing dependencies
`pip install -r requirements.txt`.

## Setting up postgresql
1. Setup postgresql from the [official documentation](https://www.postgresql.org/docs/10/static/index.html) under chapter 16/17.
1. Setup your `.pgpass` file for secure storage of password and port as explained [here](https://www.postgresql.org/docs/9.3/static/libpq-pgpass.html) or [this SO post](https://stackoverflow.com/questions/28800880/python-connect-to-postgresql-with-libpq-pgpass)  for Linux/Mac.
1. Create a file called `conn.txt` which contains the connection string for the `psycopg2` library to connect to a postgresql server. This file will contain the parameters for the connection string. For example, `host='localhost' dbname='mydbname' user='myusername'`.

## Running the app
1. Fork and then clone the repo.
1. [Install the dependencies](#Installing-dependencies).
1. [Setup the database configurations for postgresql](#Setting-up-postgresql).
1. The required configurations have been set in `.flaskenv` so run the app using `flask run`. The app will be hosted on `http://127.0.0.1:5000/` by default.
