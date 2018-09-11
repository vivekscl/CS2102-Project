-- This file contains the DDL or in other words, all the table creation scripts
CREATE TABLE if not exists items (
  ItemName varchar(256) PRIMARY KEY,
  Description varchar(128),
  Price real
);