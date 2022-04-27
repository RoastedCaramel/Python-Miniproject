from tkinter import *
from tkinter import ttk, messagebox

from app import LoginPage, DisplayCustomers
import pymysql
import Constants
import random
import numpy as np


# computer_id = random.seed(10)
# print("computer_id=", computer_id)


def manage_computer(currentlyLoggedInAdmin):
    ws = Tk()
    ws.title('Manage Computer Terminals')
    ws.geometry('380x300')
    # ws.config(bg='#0B5A81')
    # f = ('Times', 14)
    menuFont = ('Times', 12)

    # Menu Bar
    menuBar = Menu(ws, font=menuFont)

    #   Menu 1: Admin menu
    def adminLogout():
        ws.destroy()
        messagebox.showinfo('Login Status', 'You have logged out as administrator!')
        LoginPage.Login_Page()

    adminMenu = Menu(menuBar, tearoff=0)
    adminMenu.add_command(label=f"Logged in as {currentlyLoggedInAdmin}", font=('Times', 11, 'bold'), command=NONE)
    adminMenu.add_separator()
    adminMenu.add_command(label="logout", font=('Times', 11), command=adminLogout)
    menuBar.add_cascade(label="Admin", menu=adminMenu)

    #   Menu 2: Computer menu
    # computerMenu = Menu(menuBar, tearoff=0)
    # computerMenu.add_command(label="Add Computer", command=NONE)
    # computerMenu.add_command(label="Remove Computer", command=NONE)
    # menuBar.add_cascade(label='Manage Computer', menu=computerMenu)
    #   Menu 3: Registered Users Menu
    def manage_regestered_users():
        ws.destroy()
        DisplayCustomers.display_customers(currentlyLoggedInAdmin)

    registeredUsersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Registered Customers", command=manage_regestered_users, menu=registeredUsersMenu)
    #   Menu 4: Earnings Menu
    accountingMenu = Menu(menuBar, tearoff=0)
    accountingMenu.add_command(label="Daily Earning", command=NONE)
    accountingMenu.add_command(label="Monthly Earning", command=NONE)
    menuBar.add_cascade(label="Earnings", menu=accountingMenu)

    ws.config(menu=menuBar)

    # Main Frame
    main_frame = LabelFrame(
        ws,
        bd=2,
        relief=SOLID,
        text="Computer Terminals",
        font=('Times', 20)
    )
    main_frame.pack()

    Label(main_frame, text="Computer No.").grid(row=0, column=0, pady=10, padx=10)

    # Label(main_frame, text="Availability").grid(row=0, column=1, pady=10, padx=10)

    def get_computer_details():
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        cur = con.cursor()
        cur.execute("SELECT * FROM computer")
        data = cur.fetchall()
        return data

    def refresh():
        ws.destroy()
        manage_computer(currentlyLoggedInAdmin)

    def addpc():
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        cur = con.cursor()
        sql = "INSERT INTO computer(inUse) VALUES ('%s')"
        values = 'False'
        cur.execute(sql % values)
        print("Added PC")
        con.commit()
        con.close()
        refresh()

    if get_computer_details() != ():
        computer_data = get_computer_details()
    else:
        computer_data = tuple([[()], [()]])
    displayComputerInfoRowNumber = 2
    print("computer_data=", computer_data)
    xyz = np.array(computer_data)
    sliced = xyz[:, [0]]

    for i in range(len(computer_data)):
        print(computer_data, "\n\nlen=", len(computer_data))
        abc = computer_data[i][0]
        print("abc=", abc)

        def removepc(a):
            con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
            cur = con.cursor()
            sql = "DELETE FROM computer WHERE computer_id='%s'"
            removed = int(sliced[a])
            print("Removed PC:", removed)
            cur.execute(sql % removed)
            con.commit()
            con.close()
            refresh()

        if get_computer_details() != ():
            Label(main_frame, text=computer_data[i][0]).grid(row=displayComputerInfoRowNumber, column=0)
            Button(main_frame, text='Remove', bd='5', command=lambda a=i: removepc(a)).grid(
                row=displayComputerInfoRowNumber, column=1)

        # btn = Button(main_frame, text='Remove', bd='5', command=lambda a=i: removepc(a)).grid(row=displayComputerInfoRowNumber, column=1)

        # print("i=",i,"buttons=", buttons)
        # btns = Button(main_frame, text='Remove', command=removepc).grid(row=displayComputerInfoRowNumber, column=1)
        # btns.pack()
        # btns.append(button)
        # button = Button(main_frame, text='Remove', bd='5', command=removepc).grid(row=displayComputerInfoRowNumber, column=1)
        # print("buttons=====", buttons)
        displayComputerInfoRowNumber += 1
    if get_computer_details() == ():
        Label(main_frame, text='None').grid(row=displayComputerInfoRowNumber, column=0)
    Button(main_frame, text='    Add    ', bd='5', command=addpc).grid(row=displayComputerInfoRowNumber + 1,
                                                                       column=1)
    ttk.Separator(main_frame, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

    ws.mainloop()


# manage_computer('Adam')
