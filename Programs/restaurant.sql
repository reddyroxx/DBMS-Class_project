drop database restaurant_franchise;
create database restaurant_franchise;
\c restaurant_franchise


create table branch(
branch_id varchar(5) NOT NULL,
location TEXT,
contact_no varchar(10) unique,
timings TEXT,
primary key(branch_id)
);


create table owner(
owner_id TEXT,
contact_no varchar(10) not NULL UNIQUE,
name TEXT,
branch_id varchar(5) NOT NULL,
primary key(owner_id),
foreign key(branch_id) references branch
);


create table supplier (
contact_no varchar(10) NOT NULL unique,
supplier_id varchar(5),
name	TEXT,
address	TEXT,
branch_id varchar(5),
primary key(supplier_id),
foreign key(branch_id) references branch
);


CREATE TABLE employee (
employee_id varchar(10),
name TEXT,
contact_no varchar(10) NOT NULL UNIQUE,
salary INTEGER NOT NULL,
designation TEXT,
branch_id varchar(5) NOT NULL,
primary key(employee_id),
foreign key(branch_id) references branch
);


CREATE TABLE customer (
customer_id varchar(10),
name TEXT,
contact_no varchar(10) NOT NULL,
email_id TEXT,
branch_id varchar(5),
PRIMARY KEY(customer_id),
foreign key(branch_id) references branch
);







