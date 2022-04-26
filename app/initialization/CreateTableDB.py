import uuid

import pymysql
from app import Constants


def customerTable():
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE customer (user_id VARCHAR(255) PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL, email VARCHAR("
        "255) NOT NULL, contact INT NOT NULL, gender VARCHAR(7) NOT NULL, password VARCHAR(255) NOT NULL)")
    con.commit()


def adminTable():
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE admin (user_id INT PRIMARY KEY NOT NULL , name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT "
        "NULL, password VARCHAR(255) NOT NULL)")
    con.commit()


def insertingCustomers():
    for i in range(50):
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        cur = con.cursor()
        uid = uuid.uuid4()
        sql = "INSERT INTO customer(user_id, name, email, contact, gender, password) VALUES ('%s','%s','%s', '%d', '%s', '%s')"
        values = (uid,
                  f'name{i}',
                  f'emai{i}@email',
                  4125567883,
                  'male',
                  'abc123')
        cur.execute(sql % values)
        con.commit()
        con.close()


def insertingAdmins():
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    sql = "INSERT INTO admin(user_id, name, email, password) VALUES ('%d','%s','%s','%s')"
    values = (1, "Admin1", "admin1@email.com", "password1")
    cur.execute(sql % values)
    con.commit()
    con.close()


def computerTable():
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE computer (computer_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,inUse VARCHAR(10) DEFAULT 'FALSE',"
        "start_time TIME, user_id VARCHAR(255), FOREIGN KEY (user_id) REFERENCES customer (user_id))")
    con.commit()


def earningsTable():
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE session_earnings (bill_id INT computer_id INT PRIMARY KEY NOT NULL,user VARCHAR(255), user_id VARCHAR(255) FOREIGN KEY REFERENCES customer(user_id)),start_time TIME,end_time TIME")
    con.commit()

# un comment below to create tables and insert values
# customerTable()
# insertingCustomers()
# adminTable()
# insertingAdmins()
# computerTable()
