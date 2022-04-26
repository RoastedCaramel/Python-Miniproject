from tkinter import *
from tkinter import ttk, messagebox

import LoginPage


def get_computer_details():
    # computer id(int), in use(boolean), UserUsingStartTime(String),UserUsingID(String)
    data = [[1, False, '05:30', 'id1'], [2, True, '06:30', 'id2'], [3, False, '07:30', 'id3']]
    return data


def Main_Admin_Page(currentlyLoggedInAdmin):
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

    Label(main_frame, text="Computer No.").grid(row=0, column=0, pady=10, padx=10)
    Label(main_frame, text="Availability").grid(row=0, column=1, pady=10, padx=10)
    Label(main_frame, text="User").grid(row=0, column=2, pady=10, padx=10)
    Label(main_frame, text="Start Time").grid(row=0, column=3, pady=10, padx=10)
    ttk.Separator(main_frame, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')
    # TODO Add vertical separators for each column
    # ttk.Separator(main_frame, orient='vertical').grid(column=0, row=0, rows pan=2, sticky='ns')

    # Button(main_frame, text="test").grid(row=2, column=0)
    # computer id(int), in use(boolean), UserUsingStartTime(String),UserUsingID(String)
    # Fetch all computer data from database
    computer_data = get_computer_details()

    # Displaying all the computers and their information
    displayComputerInfoRowNumber = 2
    for i in range(0, len(computer_data)):
        # computer ID
        Label(main_frame, text=computer_data[i][0]).grid(row=displayComputerInfoRowNumber, column=0)
        # Check Availability
        if computer_data[i][1]:
            # Availability
            Label(main_frame, text='Available', background='green').grid(row=displayComputerInfoRowNumber, column=1)
            # User id
            Label(main_frame, text='').grid(row=displayComputerInfoRowNumber, column=2)
            # user Start Time
            Label(main_frame, text='').grid(row=displayComputerInfoRowNumber, column=3)

        else:
            Label(main_frame, text='Not Available', background='red').grid(row=displayComputerInfoRowNumber, column=1)
            # User id
            Label(main_frame, text=computer_data[i][3]).grid(row=displayComputerInfoRowNumber, column=2)
            # user Start Time
            Label(main_frame, text=computer_data[i][2]).grid(row=displayComputerInfoRowNumber, column=3)
        displayComputerInfoRowNumber += 1  # to increase the row number to display each computer

    # bg='#CCCCCC',
    # Label(
    #     main_frame,
    #     text="Computer Terminals",
    #     bg='red',
    #     font=f
    # ).grid(row=0, column=0, sticky=W, pady=10)
    ws.mainloop()

Main_Admin_Page('Adam')