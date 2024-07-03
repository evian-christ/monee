from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from add import open_add
from view import open_view
from settings import open_settings, lan

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

main.title("m0nee v0.0.1")
main.geometry("630x210+900+400")

#=====================================

tday = Label(main, text=today)
tday.grid(column=0, row=0, pady=(15, 5), padx=20, sticky='w')
summary = Label(main, text="summary")
summary.grid(column=0, row=1, pady=(5,20), padx=20, sticky='w')

bar_budget = Canvas(main, width=600, height=20)
bar_budget.grid(column=0, row=2, sticky='w', columnspan=4)
bar_budget.create_text(30,12,fill="black",text="£", font=('Arial 13 bold'))
bar_budget.create_rectangle(55,5,600,20, fill='white')
bar_budget.create_rectangle(55,5,200,20, fill='grey')

bar_time = Canvas(main, width=600, height=20)
bar_time.grid(column=0, row=3, sticky='w', columnspan=4, pady=(10, 0))
bar_time.create_text(30,15,fill="black",text="🕓", font=('10'))
bar_time.create_rectangle(55,5,600,20, fill='white')
bar_time.create_rectangle(55,5,200,20, fill='grey')

but = Frame(main)
but.grid(column=0, row=4, columnspan=4, sticky='w')

texts = [
    ["New", "추가"],
    ["View", "내역"],
    ["Stats", "통계"],
    ["Settings", "설정"]
]

btn_add = Button(but, text = texts[0][lan], command = open_add)
btn_view = Button(but, text = texts[1][lan], command = open_view)
btn_stats = Button(but, text = texts[2][lan], state=DISABLED)
btn_settings = Button(but, text = texts[3][lan], command = open_settings)

btn_add.grid(column=0, row=4, pady=5, padx=(20, 10))
btn_view.grid(column=1, row=4, pady=25, padx=10)
btn_stats.grid(column=2, row=4, pady=5, padx=10)
btn_settings.grid(column=3, row=4, pady=5, padx=10)

main.mainloop()