import uuid
import random
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
        sql = "INSERT INTO customer(user_id, name, email, contact, gender, password) VALUES ('%s','%s','%s', '%d', "
        "'%s', '%s')"
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
        "CREATE TABLE session_earnings (bill_id INT PRIMARY KEY AUTO_INCREMENT, computer_id INT, FOREIGN KEY "
        "(computer_id) REFERENCES computer (computer_id),user_id VARCHAR(255), FOREIGN KEY (user_id) REFERENCES "
        "customer(user_id), date DATE, earning INT)")
    con.commit()


def insertEarnings():
    for i in range(50):
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        cur = con.cursor()
        uid = uuid.uuid4()
        sql = "INSERT INTO session_earnings(computer_id, user_id, date, earning) VALUES ('%d','%s', current_date(), '%d')"
        values = (1,
                  '000b308e-f9e7-4fb8-83fc-5c17ba9ed98b',
                  random.randrange(50, 150))
        cur.execute(sql % values)
        con.commit()
        con.close()

# un comment below to create tables and insert values
# customerTable()
# insertingCustomers()
# adminTable()
# insertingAdmins()
# computerTable()
# earningsTable()
# insertEarnings()
