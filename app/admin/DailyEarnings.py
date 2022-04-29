from tkinter import *
from tkinter import ttk, messagebox
import datetime
import pymysql

from app.util import Constants


def fetch_daily_earning_data():
    try:
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        c.execute("Select * from session_earnings WHERE DATE(date) = CURDATE()")
        earningData = c.fetchall()
        return earningData
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")


def fetch_monthly_earning_data():
    try:
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        c.execute("Select * from session_earnings WHERE MONTH(date) = MONTH(CURDATE())")
        earningData = c.fetchall()
        return earningData
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")


def daily_monthly_earnings(currentlyLoggedInAdmin, typeOfReq):
    ws = Tk()
    ws.title('Daily Earnings')
    ws.geometry('550x330')
    ws.config(padx=10, pady=10)
    menuFont = ('Times', 12)

    # Menu Bar
    menuBar = Menu(ws, font=menuFont)

    #   Menu 1: Admin menu
    def adminLogout():
        ws.destroy()
        messagebox.showinfo('Successfully Logged out', 'You have logged out as administrator!')
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

    #   Menu 2: Computer menu
    def manage_computers():
        ws.destroy()
        from ManageComputer import manage_computer
        manage_computer(currentlyLoggedInAdmin)

    computerMenu = Menu(menuBar, tearoff=0)
    computerMenu.add_command(label="Manage Computer", command=manage_computers)
    menuBar.add_cascade(label='Computer', menu=computerMenu)

    #   Menu 3: Registered Users Menu
    def manage_regestered_users():
        from DisplayCustomers import display_customers
        ws.destroy()
        display_customers(currentlyLoggedInAdmin)

    registeredUsersMenu = Menu(menuBar, tearoff=0)
    registeredUsersMenu.add_command(label='Manage Customers', command=manage_regestered_users)
    menuBar.add_cascade(label="Registered Customers", menu=registeredUsersMenu)

    #   Menu 4: Earnings Menu
    if typeOfReq == 0:
        def manage_monthly_earnings():
            ws.destroy()
            daily_monthly_earnings(currentlyLoggedInAdmin, 1)

        accountingMenu = Menu(menuBar, tearoff=0)
        accountingMenu.add_command(label="Monthly Earning", command=manage_monthly_earnings)
    if typeOfReq == 1:
        def manage_daily_earnings():
            ws.destroy()
            daily_monthly_earnings(currentlyLoggedInAdmin, 0)

        accountingMenu = Menu(menuBar, tearoff=0)
        accountingMenu.add_command(label="Daily Earning", command=manage_daily_earnings)
    menuBar.add_cascade(label="Earnings", menu=accountingMenu)

    ws.config(menu=menuBar)

    # Main Frame
    currentDateMonth = datetime.datetime.now()
    monthName = currentDateMonth.strftime("%B")
    currentDate = datetime.date.today()
    if typeOfReq == 0:
        textLabel = f"Earnings for : {currentDate}"
    elif typeOfReq == 1:
        textLabel = f"Monthly Earnings for {monthName}"
    main_frame = LabelFrame(
        ws,
        bd=2,
        relief=SOLID,
        text=textLabel,
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
    if typeOfReq == 0:
        earningData = fetch_daily_earning_data()
    elif typeOfReq == 1:
        earningData = fetch_monthly_earning_data()

    amountEarned = 0
    for i in earningData:
        trv.insert('', 'end', iid=i[0], text=i[0], values=(i[0], i[3], i[4], i[1], i[2]))
        amountEarned += i[4]
    Label(main_frame, text=f"Amount Earned  =  ₹{amountEarned}", font=('Sans', 20)).pack(side='bottom')
    ws.mainloop()
