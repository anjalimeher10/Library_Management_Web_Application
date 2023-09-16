# Libaray_Management_Web_Application
App.py is main file

-install flask
pip install flask

-install mysql connector
pip install mysql.connector

connection to local DB by using mysql.connector
set your user  in DB and create a database "amx" 
create tables(user, books, givenbook)

#sql query 
create table user
create table user (email nvarchar(100) , password int);

create table books
create table books(book_id int, book_name varchar(50) , book_anthor varchar(50) , book_rent int);

create table givenbook
create table givenbook(book_id int, book_name varchar(100) , member_name(50),book_rent int,book_anthor varchar(50) );


