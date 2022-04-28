import uuid
from tkinter import *
from tkinter import messagebox

import pymysql

import Constants


def validation(register_name, register_email, register_mobile, var, register_pwd, pwd_again):
    check_counter = 0
    warn = ""

    if register_name.get() == "":
        warn = "Name can't be empty"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1
    # check_counter = 0

    if register_email.get() == "":
        warn = "Email can't be empty"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if register_mobile.get() == "":
        warn = "Contact can't be empty"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if var.get() == "":
        warn = "Select Gender"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if register_pwd.get() == "":
        warn = "Password can't be empty"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if pwd_again.get() == "":
        warn = "Re-enter password can't be empty"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if register_pwd.get() != pwd_again.get():
        warn = "Passwords didn't match!"
        messagebox.showerror("Error Registering", warn)
    else:
        check_counter += 1

    if check_counter == 7:
        return True


def registeringUser(register_name, register_email, register_mobile, var, register_pwd, pwd_again, ws):
    # getting details
    validated = validation(register_name, register_email, register_mobile, var, register_pwd, pwd_again)
    if validated:
        print("Validation successful")
        uid = uuid.uuid4()
        userName = register_name.get()
        userEmail = register_email.get()
        userMobile = int(register_mobile.get())
        userPassword = register_pwd.get()
        userGender = var.get()

        try:
            con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
            cur = con.cursor()
            sql = "INSERT INTO customer(user_id, name, email, contact, gender, password) VALUES ('%s','%s','%s', '%d', '%s', '%s')"
            values = (uid,
                      userName,
                      userEmail,
                      userMobile,
                      userGender,
                      userPassword)
            cur.execute(sql % values)
            con.commit()
            con.close()
        except EXCEPTION as e1:
            messagebox.showerror("Error Registering",
                                 f"An Unexpected error occurred while registering. Please try again. Exception:{e1}")
        ws.destroy()
        from app.LoginPage import Login_Page
        Login_Page()


def Registeration_Page():
    ws = Tk()
    ws.title('Registration Page')
    ws.config(bg='#0B5A81')

    f = ('Times', 14)
    var = StringVar()
    var.set('male')

    right_frame = Frame(
        ws,
        bd=2,
        bg='#CCCCCC',
        relief=SOLID,
        padx=10,
        pady=10
    )

    Label(
        right_frame,
        text="Enter Name",
        bg='#CCCCCC',
        font=f
    ).grid(row=0, column=0, sticky=W, pady=10)

    Label(
        right_frame,
        text="Enter Email",
        bg='#CCCCCC',
        font=f
    ).grid(row=1, column=0, sticky=W, pady=10)

    Label(
        right_frame,
        text="Contact Number",
        bg='#CCCCCC',
        font=f
    ).grid(row=2, column=0, sticky=W, pady=10)

    Label(
        right_frame,
        text="Select Gender",
        bg='#CCCCCC',
        font=f
    ).grid(row=3, column=0, sticky=W, pady=10)

    Label(
        right_frame,
        text="Enter Password",
        bg='#CCCCCC',
        font=f
    ).grid(row=5, column=0, sticky=W, pady=10)

    Label(
        right_frame,
        text="Re-Enter Password",
        bg='#CCCCCC',
        font=f
    ).grid(row=6, column=0, sticky=W, pady=10)

    gender_frame = LabelFrame(
        right_frame,
        bg='#CCCCCC',
        padx=10,
        pady=10,
    )

    register_name = Entry(
        right_frame,
        font=f
    )

    register_email = Entry(
        right_frame,
        font=f
    )

    register_mobile = Entry(
        right_frame,
        font=f
    )

    male_rb = Radiobutton(
        gender_frame,
        text='Male',
        bg='#CCCCCC',
        variable=var,
        value='male',
        font=('Times', 10),

    )

    female_rb = Radiobutton(
        gender_frame,
        text='Female',
        bg='#CCCCCC',
        variable=var,
        value='female',
        font=('Times', 10),

    )

    others_rb = Radiobutton(
        gender_frame,
        text='Others',
        bg='#CCCCCC',
        variable=var,
        value='others',
        font=('Times', 10)

    )

    register_pwd = Entry(
        right_frame,
        font=f,
        show='*'
    )
    pwd_again = Entry(
        right_frame,
        font=f,
        show='*'
    )

    def reg():
        registeringUser(register_name, register_email, register_mobile, var, register_pwd, pwd_again, ws)

    def login():
        ws.destroy()
        from app.LoginPage import Login_Page
        Login_Page()

    register_btn = Button(
        right_frame,
        width=15,
        text='Register',
        font=f,
        relief=SOLID,
        cursor='hand2',
        command=reg
    )

    login_btn = Button(
        right_frame,
        width=15,
        text='Back To Login',
        font=f,
        relief=SOLID,
        cursor='hand2',
        command=login
    )

    register_name.grid(row=0, column=1, pady=10, padx=20)
    register_email.grid(row=1, column=1, pady=10, padx=20)
    register_mobile.grid(row=2, column=1, pady=10, padx=20)
    register_pwd.grid(row=5, column=1, pady=10, padx=20)
    pwd_again.grid(row=6, column=1, pady=10, padx=20)
    register_btn.grid(row=7, column=1, pady=10, padx=20)
    login_btn.grid(row=7, column=0, pady=10, padx=20)
    right_frame.pack()

    gender_frame.grid(row=3, column=1, pady=10, padx=20)
    male_rb.pack(expand=True, side=LEFT)
    female_rb.pack(expand=True, side=LEFT)
    others_rb.pack(expand=True, side=LEFT)

    ws.mainloop()
