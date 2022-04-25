from datetime import datetime, date

# to get current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
# to get current date
today = date.today()
print("Today's date:", today)
