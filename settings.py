from tkinter import *
from tkinter.ttk import *
from dateAndTime import *

import json
import os

#=====================================

settings = {
    "month_start_date": "1",
    "category": ["Food", "Entertainment", "Transport", "Misc"],
    "Budget": ["550", "150", "100", "100"]
}

if not os.path.exists('config.json'):
    with open('config.json', 'w') as config_file:
        json.dump(settings, config_file)
else:
    with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

#=====================================

def open_settings():
    root = Tk()

    root.title("Settings")
    root.geometry("500x500+800+300")

    notebook = Notebook(root, padding=10)

    #=====================================

    tab1 = Frame(notebook, padding=50)
    notebook.add(tab1, text="General")
    startdaylb = Label(tab1, text = "Start day of month: ")
    startday = Combobox(
        tab1,
        width=2,
        state="readonly",
        values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    )
    startdaylb.grid(column=0, row=0)
    startday.grid(column=1, row=0)

    #=====================================

    tab2 = Frame(notebook, padding=50)
    notebook.add(tab2, text="Category")
    categorylb = Label(tab2, text="Categories: ")
    category = Listbox(tab2)
    category_edit = Button(tab2, text='edit')
    category_add = Button(tab2, text="+", width=5)
    category_del = Button(tab2, text="-", width=5)
    categorylb.grid(column=0, row=0, sticky='w', pady=5)
    category.grid(column=0, row=1, columnspan=3, sticky='nswe')
    category_edit.grid(column=0, row=2, sticky='w', pady=5)
    category_add.grid(column=1, row=2, sticky='e')
    category_del.grid(column=2, row=2, sticky='e')

    for i in settings['category']:
        category.insert(END, i)

    #=====================================

    notebook.grid(sticky='nswe')

    root.mainloop()