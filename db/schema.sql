-- This file contains the DDL or in other words, all the table creation scripts
CREATE TABLE if not exists users (
  id SERIAL PRIMARY KEY,
  username varchar(128) UNIQUE NOT NULL,
  name varchar(128) NOT NULL,
  password_hash varchar(128) NOT NULL,
  phonenumber char(8)
);