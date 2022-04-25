from datetime import datetime
from time import strftime
from tkinter import *

import Constants
import LoginPage
import pymysql


def fetch_user_data(uid, current_time):
    global data
    print(uid, current_time)
    # Fetching currently logged in customer data
    try:
        data = []
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        c.execute(f"Select * from customer WHERE user_id = '{uid}'")
        data = c.fetchall()
        con.close()
    except EXCEPTION as e:
        print(e)
    return data[0]


def add_logout_data_to_db():
    try:
        now = datetime.now()
        end_time = now.strftime("%H:%M:%S")
        data = []
    except EXCEPTION as e:
        print(e)


def Customer_Page(uid):
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")
    user_data = []
    user_data = fetch_user_data(uid, start_time)
    print(user_data[1])
    ws = Tk()
    ws.title('Cyber Cafe Management App')
    ws.config(bg='#0B5A81')  # window background
    ws.geometry('350x300')

    f = ('Times', 14)
    frame = Frame(
        ws,
        bd=2,
        bg='#CCCCCC',  # background for the frame
        relief=SOLID,
        padx=10,
        pady=10
    )
    Label(
        ws,
        text=f"Welcome {user_data[1]}",
        bg='#CCCCCC',
        font=('Times', 20)).grid(row=0, column=0, columnspan=2, sticky=N, padx=50, pady=10)

    def logout():
        ws.destroy()
        add_logout_data_to_db()
        # LoginPage.Login_Page()
        # TODO display bill and add earnings to database
        return

    logout_btn = Button(
        ws,
        width=15,
        text='End Session',
        font=f,
        relief=SOLID,
        cursor='hand2',
        command=logout
    )
    logout_btn.grid(row=1, columnspan=2)
    ws.mainloop()
    #
    # Label(
    #     left_frame,
    #     text="Enter Email",
    #     bg='#CCCCCC',
    #     font=f).grid(row=1, column=0, pady=10)
    #
    # Label(
    #     left_frame,
    #     text="Enter Password",
    #     bg='#CCCCCC',
    #     font=f
    # ).grid(row=2, column=0, pady=10)
    #
    # email_tf = Entry(
    #     left_frame,
    #     font=f
    # )
    # pwd_tf = Entry(
    #     left_frame,
    #     font=f,
    #     show='*'
    #


# Customer_Page('fa04be85-1077-4d99-aac1-28f18d205098')
