from tkinter import *
from tkinter import messagebox
import Constants

import pymysql

import CustomerPage
import MainAdminPage
# importing all different pages used
import RegisterationPage


def login_response(email_tf, pwd_tf, ws):
    warn, userEmail, pwd, uid, userData, adminData, adminPassword, adminEmail, adminName, adminID \
        = '', [], [], [], [], [], [], [], [], []
    try:
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        r = con.cursor()
        userData = []
        c.execute("Select * from customer")
        r.execute("Select * from admin")
        userData = c.fetchall()
        adminData = r.fetchall()
        # print(userData)
        uid = [0] * len(userData)
        userEmail = [0] * len(userData)
        pwd = [0] * len(userData)
        adminID = [0] * len(adminData)
        adminEmail = [0] * len(adminData)
        adminPassword = [0] * len(adminData)
        adminName = [0] * len(adminData)
        for row in range(0, len(userData)):
            uid[row] = userData[row][0]
            userEmail[row] = userData[row][2]
            pwd[row] = userData[row][5]
        for row in range(0, len(adminData)):
            adminID[row] = adminData[row][0]
            adminName[row] = adminData[row][1]
            adminEmail[row] = adminData[row][2]
            adminPassword[row] = adminData[row][3]
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")
    enteredEmail = email_tf.get()
    enteredPassword = pwd_tf.get()
    check_counter = 0
    if enteredEmail == "":
        warn = "Username can't be empty"
    else:
        check_counter += 1
    if enteredPassword == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1
    if check_counter == 2:

        for i in range(0, len(userData)):
            if enteredEmail == userEmail[i] and enteredPassword == pwd[i]:
                ws.destroy()
                messagebox.showinfo('Login Status', 'Logged in Successfully!')
                # TODO Send the customer_uid[i] to the next page when login successful for customer and display the page
                # now = datetime.now()
                # current_time = now.strftime("%H:%M:%S")
                CustomerPage.Customer_Page(uid[i])

        for i in range(0, len(adminData)):
            if enteredEmail == adminEmail[i] and enteredPassword == adminPassword[i]:
                loggedInAdminName = adminName[i]
                loggedInAdminId = adminID[i]
                messagebox.showinfo('Login Status', 'Logged in Successfully as Admin!')
                # TODO Send the admin_uid[i] to the next page when login successful for admin and display the page
                ws.destroy()
                MainAdminPage.Main_Admin_Page(loggedInAdminName)
                break
        else:
            messagebox.showerror('Login Status', 'invalid userEmail or password')
    else:
        messagebox.showerror('', warn)


def Login_Page():
    ws = Tk()
    ws.title('Cyber Cafe Management App')
    ws.config(bg='#0B5A81')  # window background

    f = ('Times', 14)
    left_frame = Frame(
        ws,
        bd=2,
        bg='#CCCCCC',  # background for the frame
        relief=SOLID,
        padx=10,
        pady=10
    )

    Label(
        left_frame,
        text="Welcome",
        bg='#CCCCCC',
        font=('Times', 20)).grid(row=0, column=0, columnspan=2, sticky=N, pady=10)

    Label(
        left_frame,
        text="Enter Email",
        bg='#CCCCCC',
        font=f).grid(row=1, column=0, pady=10)

    Label(
        left_frame,
        text="Enter Password",
        bg='#CCCCCC',
        font=f
    ).grid(row=2, column=0, pady=10)

    email_tf = Entry(
        left_frame,
        font=f
    )
    pwd_tf = Entry(
        left_frame,
        font=f,
        show='*'
    )

    def login():
        login_response(email_tf, pwd_tf, ws)

    def reg():
        ws.destroy()
        RegisterationPage.Registeration_Page()

    register_btn = Button(
        left_frame,
        width=15,
        text='Register',
        font=f,
        relief=SOLID,
        cursor='hand2',
        command=reg
    )
    login_btn = Button(
        left_frame,
        width=15,
        text='Login',
        font=f,
        relief=SOLID,
        cursor='hand2',
        command=login  # login the user
    )

    email_tf.grid(row=1, column=1, pady=10, padx=20)
    pwd_tf.grid(row=2, column=1, pady=10, padx=20)
    login_btn.grid(row=3, column=1, pady=10, padx=20)
    register_btn.grid(row=3, column=0, pady=10, padx=20)
    left_frame.pack()

    ws.mainloop()
