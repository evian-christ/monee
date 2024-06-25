from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from add import open_add
from view import open_view

import sqlite3
import json
import os

default_settings = {
    "month_start_date": "1",
    "category": ["Food", "Entertainment", "Transport", "Misc"],
    "Budget": ["550", "150", "100", "100"]
}

if not os.path.exists('config.json'):
    with open('config.json', 'w') as config_file:
        json.dump(default_settings, config_file)

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

#=====================================

main = Tk()
main.grid_columnconfigure(0, weight=1)

main.title("monee v0.0.1")
main.geometry("250x305+900+400")

#=====================================

tday = Label(main, text = today)
tday.grid(pady=7, sticky='n')

btn_add = Button(main, text = "Add", padding=10, command = open_add)
btn_view = Button(main, text = "View", padding=10, command = open_view)
btn_settings = Button(main, text = "Settings", padding=10, command = open_add)

btn_add.grid(column = 0, row = 2, pady = 10)
btn_view.grid(column = 0, row = 3, pady = 10)
btn_settings.grid(column = 0, row = 4, pady = 10)

main.mainloop()