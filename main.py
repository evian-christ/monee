from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from add import open_add
from view import open_view
from settings import open_settings

import sqlite3

dbc = sqlite3.connect('data.db')

dbc.execute('''
CREATE TABLE if not exists expenses
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER,
            name VARCHAR(32),
            cost REAL,
            rate INTEGER,
            desc VARCHAR(255),
            category VARCHAR(32),
            remark VARCHAR(255)
            )
''')

#=====================================

main = Tk()
#main.grid_columnconfigure(0, weight=1)

main.title("monee v0.0.1")
main.geometry("700x305+900+400")

#=====================================

tday = Label(main, text=today)
tday.grid(column=0, row=0, pady=(15, 5), padx=10)
summary = Label(main, text="summary")
summary.grid(column=0, row=1, pady=(5,10), padx=10)

btn_add = Button(main, text = "New", command = open_add)
btn_view = Button(main, text = "View", command = open_view)
btn_stats = Button(main, text = "Stats", state=DISABLED)
btn_settings = Button(main, text = "Settings", command = open_settings)

btn_add.grid(column=0, row=4, pady=5, padx=(20, 10))
btn_view.grid(column=1, row=4, pady=5, padx=10)
btn_stats.grid(column=2, row=4, pady=5, padx=10)
btn_settings.grid(column=3, row=4, pady=5, padx=10)

main.mainloop()