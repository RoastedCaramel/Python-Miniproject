from datetime import datetime
from tkinter import *
import time
from tkinter import messagebox

from app.util import Constants
import pymysql

timeInSeconds = 0
totalAmount = 0

counter = 66600
running = False


def fetch_user_data(uid):
    global data
    # Fetching currently logged in customer data
    try:
        data = []
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        c = con.cursor()
        c.execute(f"Select * from customer WHERE user_id = '{uid}'")
        data = c.fetchall()
        con.close()
    except Exception as ep:
        messagebox.showerror(f"Error: {ep}")
    return data[0]


def add_logout_data_to_db(uid, totalAmount):
    con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
    cur = con.cursor()
    sql = "INSERT INTO session_earnings(computer_id, user_id, date, earning) VALUES ('%d','%s', current_date(), '%d')"
    values = (1,
              uid,
              totalAmount)
    print(totalAmount)
    cur.execute(sql % values)
    con.commit()
    con.close()


def remove_user_data_from_computer(enteredComputerId):
    try:
        print(enteredComputerId)
        con = pymysql.connect(host=Constants.HOST, user=Constants.USER, db=Constants.DATABASE)
        cur = con.cursor()
        sql = f"UPDATE computer SET inUse = 'False', start_time = '', user_id ='' WHERE computer_id = {enteredComputerId}"
        cur.execute(sql)
        con.commit()
        con.close()
    except EXCEPTION as e1:
        messagebox.showerror("Logging Out",
                             f"An Unexpected error occurred while Logging Out. Please try again. Exception:{e1}")


def Customer_Page(uid, computerId):
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")
    user_data = []
    user_data = fetch_user_data(uid)
    print(user_data[1])

    ws = Tk()
    ws.title('Cyber Cafe Management App')
    ws.config(bg='#0B5A81')  # window background
    ws.geometry('300x300')

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
        font=('Times', 20)).grid(row=0, column=0, columnspan=2, sticky=N, padx=60, pady=10)

    def counter_label(label):
        def count():
            if running:
                global counter

                # To manage the initial delay.
                if counter == 66600:
                    display = "Starting..."
                else:
                    tt = datetime.fromtimestamp(counter)
                    string = tt.strftime("%H:%M:%S")
                    display = string

                    # print(display)

                    def get_sec(string):

                        H, M, S = string.split(':')
                        return int(H) * 3600 + int(M) * 60 + int(S)

                    global timeInSeconds
                    timeInSeconds = int(get_sec(string))
                    global totalAmount
                    bill = 0.027 * timeInSeconds
                    totalAmount = bill

                label['text'] = display  # Or label.config(text=display)

                label.after(1000, count)
                counter += 1

        # Triggering the start of the counter.
        count()

    # print(timeInSeconds)

    def logout():
        ws.destroy()
        add_logout_data_to_db(uid, totalAmount)

        def NewWindow():
            window = Tk()
            window.title("Bill")
            window.geometry('915x490')
            bill_text_area = Text(window, font=("arial", 12))
            yt = "\t\t\t\tCyber Cafe Management System\n\t\t\t\tHarshad Mehta, Malad-400064\n"
            yt += "\t\t\t\tGST.NO:- 123456789\n"
            yt += "-" * 61 + "BILL" + "-" * 61 + "\nDate:- "

            # Date and time
            t = time.localtime(time.time())
            week_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday",
                             6: "Sunday"}
            yt += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
            yt += " " * 10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

            seconds = timeInSeconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            timeDisplayed = "%d:%02d:%02d" % (hour, minutes, seconds)
            yt += f"\nCustomer Name:- {user_data[1]}\nCustomer Contact:- {user_data[3]} \n"
            yt += "-" * 130 + "\n" + " " * 4 + "PARTICULARS\t\t\tTIME\t\tRATE\t\tAMOUNT\n"
            yt += "\n" + " " * 4 + f"PC Usage\t\t\t{timeDisplayed} \t\t100/hr\t\t{totalAmount}\n"
            yt += "-" * 130 + "\n"
            newlabel = Label(window, text="Settings Window")
            newlabel.pack()
            yt += f"\n\t\t\tTotal price :{totalAmount}\n"  # totalPrice
            bill_text_area.insert(1.0, yt)
            bill_text_area.pack(expand=True, fill=BOTH)
            remove_user_data_from_computer(computerId)
            window.focus_set()
            window.protocol("WM_DELETE_WINDOW")
            window.mainloop()

        NewWindow()
        import LoginPage
        LoginPage.Login_Page()
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
    logout_btn.place(x=75, y=190)

    label = Label(ws, width=15, bg='#116562', fg='red', font=('Times', 20))
    label.place(x=70, y=190)
    label.grid(row=0, column=0, sticky=W, padx=40, pady=120)
    running = True
    counter_label(label)

    ws.mainloop()
