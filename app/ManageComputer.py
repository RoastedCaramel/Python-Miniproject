from tkinter import *
from tkinter import ttk, messagebox


def manage_computer():
    ws = Tk()
    ws.title('Management Page')
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
    computerMenu = Menu(menuBar, tearoff=0)
    computerMenu.add_command(label="Add Computer", command=NONE)
    computerMenu.add_command(label="Remove Computer", command=NONE)
    menuBar.add_cascade(label='Manage Computer', menu=computerMenu)
    #   Menu 3: Registered Users Menu
    registeredUsersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Registered Customers", command=NONE, menu=registeredUsersMenu)
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
