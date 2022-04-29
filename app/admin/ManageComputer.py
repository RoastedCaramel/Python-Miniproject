from tkinter import *
from tkinter import ttk, messagebox

import pymysql
from app.util import Constants
import numpy as np


def manage_computer(currentlyLoggedInAdmin):
    ws = Tk()
    ws.title('Manage Computer Terminals')
    ws.geometry('380x300')
    menuFont = ('Times', 12)

    # Menu Bar
    menuBar = Menu(ws, font=menuFont)

    #   Menu 1: Admin menu
    def adminLogout():
        ws.destroy()
        messagebox.showinfo('Login Status', 'You have logged out as administrator!')
        from LoginPage import Login_Page
        Login_Page()

    def mainPage():
        ws.destroy()
        from MainAdminPage import Main_Admin_Page
        Main_Admin_Page(currentlyLoggedInAdmin)

    adminMenu = Menu(menuBar, tearoff=0)
    adminMenu.add_command(label=f"Logged in as {currentlyLoggedInAdmin}", font=('Times', 11, 'bold'), command=NONE)
    adminMenu.add_separator()
    adminMenu.add_command(label="Main Page", font=('Times', 11), command=mainPage)
    adminMenu.add_command(label="logout", font=('Times', 11), command=adminLogout)
    menuBar.add_cascade(label="Admin", menu=adminMenu)

    #   Menu 3: Registered Users Menu
    def manage_regestered_users():
        from DisplayCustomers import display_customers
        ws.destroy()
        display_customers(currentlyLoggedInAdmin)

    registeredUsersMenu = Menu(menuBar, tearoff=0)
    registeredUsersMenu.add_command(label='Manage Customers', command=manage_regestered_users)
    menuBar.add_cascade(label="Registered Customers", menu=registeredUsersMenu)

    #   Menu 4: Earnings Menu
    from DailyEarnings import daily_monthly_earnings

    def manage_monthly_earnings():
        ws.destroy()
        daily_monthly_earnings(currentlyLoggedInAdmin, 1)

    def manage_daily_earnings():
        ws.destroy()
        daily_monthly_earnings(currentlyLoggedInAdmin, 0)

    accountingMenu = Menu(menuBar, tearoff=0)
    accountingMenu.add_command(label="Daily Earning", command=manage_daily_earnings)
    accountingMenu.add_command(label="Monthly Earning", command=manage_monthly_earnings)
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

        displayComputerInfoRowNumber += 1
    if get_computer_details() == ():
        Label(main_frame, text='None').grid(row=displayComputerInfoRowNumber, column=0)
    Button(main_frame, text='    Add    ', bd='5', command=addpc).grid(row=displayComputerInfoRowNumber + 1,
                                                                       column=1)
    ttk.Separator(main_frame, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

    ws.mainloop()
