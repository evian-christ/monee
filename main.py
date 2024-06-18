from tkinter.ttk import *
from ttkthemes import ThemedTk
from dateAndTime import *
import time

import sqlite3

#-------------------DB---------------------
dbc = sqlite3.connect('data.db')

dbc.execute('''
CREATE TABLE if not exists expenses
            (
            id INTEGER PRIMARY KEY,
            date INTEGER,
            name VARCHAR(32),
            cost REAL,
            rate INTEGER,
            desc VARCHAR(255),
            category VARCHAR(32),
            remark VARCHAR(255)
            )
''')

date = time.mktime(datetime.datetime.now().timetuple())
name = "Lunch"
cost = 3.40
rate = 5
desc = "Tesco Meal Deal"
category = "Food"
remark = ""

dbc.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (date, name, cost, rate, desc, category, remark))

dbc.commit()

#----------------main window----------------
main = ThemedTk(theme='yaru')
main.grid_columnconfigure(0, weight=1)

#------------------STYLE--------------------
s = Style()
s.configure('main.TButton', font = ('Consolas', 20))

#------------------Title--------------------
main.title("monee v0.0.1")
#-------------------Size--------------------
main.geometry("250x305")

#-------------------Date--------------------
tday = Label(main, text = today, font=('Consolas', 20))
tday.grid(pady=7, sticky='n')

#-----------------function------------------
def open_add():
    addWindow = ThemedTk(theme='yaru')

    addWindow.title("Add New Entry")

    addWindow.geometry("720x360")

def open_view():
    viewWindow = ThemedTk(theme='yaru')

    viewWindow.title("View history")

    viewWindow.geometry("1080x720")

#------------------button--------------------
btn_add = Button(main, text = "Add", style = 'main.TButton', padding=10, command = open_add)
btn_view = Button(main, text = "View", style = 'main.TButton', padding=10, command = open_view)
btn_settings = Button(main, text = "Settings", style = 'main.TButton', padding=10, command = open_add)

#--------------set button grid---------------
btn_add.grid(column = 0, row = 2, pady = 10)
btn_view.grid(column = 0, row = 3, pady = 10)
btn_settings.grid(column = 0, row = 4, pady = 10)

#---------------Execute TkInter--------------
main.mainloop()