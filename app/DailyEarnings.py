from tkinter import *
from tkinter import ttk, messagebox
import datetime
import pymysql

import LoginPage
from app import DisplayCustomers, Constants
from app.ManageComputer import manage_computer


def fetch_daily_earning_data():
    try:
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        c.execute("Select * from session_earnings WHERE DATE(date) = CURDATE()")
        earningData = c.fetchall()
        return earningData
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")


def daily_earnings(currentlyLoggedInAdmin):
    ws = Tk()
    ws.title('Daily Earnings')
    ws.geometry('550x300')
    ws.config(padx=10, pady=10)
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
    def manage_computers():
        ws.destroy()
        manage_computer(currentlyLoggedInAdmin)

    computerMenu = Menu(menuBar, tearoff=0)
    computerMenu.add_command(label="Manage Computer", command=manage_computers)
    menuBar.add_cascade(label='Computer', menu=computerMenu)

    #   Menu 3: Registered Users Menu
    def manage_regestered_users():
        ws.destroy()
        DisplayCustomers.display_customers(currentlyLoggedInAdmin)

    registeredUsersMenu = Menu(menuBar, tearoff=0)
    registeredUsersMenu.add_command(label='Manage Customers', command=manage_regestered_users)
    menuBar.add_cascade(label="Registered Customers", menu=registeredUsersMenu)
    #   Menu 4: Earnings Menu
    accountingMenu = Menu(menuBar, tearoff=0)
    # accountingMenu.add_command(label="Daily Earning", command=NONE)
    accountingMenu.add_command(label="Monthly Earning", command=NONE)
    menuBar.add_cascade(label="Earnings", menu=accountingMenu)

    ws.config(menu=menuBar)

    # Main Frame
    main_frame = LabelFrame(
        ws,
        bd=2,
        relief=SOLID,
        text=f"Daily Earnings : {datetime.date.today()}",
        font=('Times', 20)
    )
    main_frame.pack(fill='x')
    trv = ttk.Treeview(main_frame, selectmode='browse')
    trv.pack(pady=10, padx=10, fill='both')
    trv["columns"] = ('1', '2', '3', '4', '5')
    trv['show'] = 'headings'
    trv.column('1', width=40, anchor='c')
    trv.column('2', width=80, anchor='c')
    trv.column('3', width=100, anchor='c')
    trv.column('4', width=80, anchor='c')
    trv.column('5', width=180, anchor='c')
    trv.heading('1', text='Bill Id')
    trv.heading('2', text='Date')
    trv.heading('3', text='Amount Earned')
    trv.heading('4', text='Computer ID')
    trv.heading('5', text='User Id')
    # my_scrollbar = ttk.Scrollbar(, orient=VERTICAL, command=trv.yview)
    # my_scrollbar.pack(side=RIGHT, fill=Y)
    earningData = fetch_daily_earning_data()
    for i in earningData:
        trv.insert('', 'end', iid=i[0], text=i[0], values=(i[0], i[3], i[4], i[1], i[2]))
    ws.mainloop()


# daily_earnings('adam')
