from tkinter import *
from tkinter import ttk, messagebox

import pymysql
import Constants


def fetch_all_registered_users():
    try:
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        userData = []
        c.execute("Select user_id,name from customer")
        userData = c.fetchall()
        return userData
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")


def display_customers(currentlyLoggedInAdmin):
    ws = Tk()
    ws.title('Registered Customers')
    ws.geometry('500x300')
    ws.config(padx=10)
    # f = ('Times', 14)
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
        text="Registered Customers",
        font=('Times', 20),
        padx=10,
    )
    main_frame.pack(padx=5, pady=5, fill='x')
    userData = fetch_all_registered_users()
    uid = [0] * len(userData)
    uname = [0] * len(userData)
    for row in range(0, len(userData)):
        uid[row] = userData[row][0]
        uname[row] = userData[row][1]
    Label(main_frame, text="Enter no to delete customer").pack()
    delete_customer = Entry(main_frame)
    # delete_customer.grid(column=1, row=1)
    delete_customer.pack()
    Button(main_frame, text="REVOKE", background='red', foreground='white',
           command=lambda: remove_customer(delete_customer)).pack()
    # Canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH)
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>',
                   lambda e:
                   my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor='nw')

    def refresh():
        ws.destroy()
        display_customers(currentlyLoggedInAdmin)

    def remove_customer(row_number):
        row_no = int(str(row_number.get()))
        print(type(row_no))
        print(uid[row_no])
        try:
            con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
            c = con.cursor()
            sql = f"DELETE FROM customer WHERE user_id='{uid[row_no]}'"
            c.execute(sql)
            con.commit()
            con.close()
        except Exception as ep:
            messagebox.showerror(f"Error: {ep}")
        refresh()

    Label(second_frame, text='No.').grid(row=0, column=0, padx=50, sticky='n')
    Label(second_frame, text="Customer Name").grid(row=0, padx=50, column=1, sticky='n')
    for customer in range(len(userData)):
        Label(second_frame, text=customer).grid(row=customer + 1, column=0, pady=5, padx=5)
        Label(second_frame, text=uname[customer]).grid(row=customer + 1, column=1, pady=5, padx=5)

    ws.mainloop()
