from tkinter import *
from tkinter.ttk import *

import sqlite3

def open_add():
    def on_submit():
        date_value = date.get()
        name_value = name.get()
        ctgr_value = ctgr.get()
        cost_value = cost.get()
        rate_value = rate.get()
        desc_value = desc.get()
        rmrk_value = rmrk.get()

        dbc = sqlite3.connect('data.db')

        dbc.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                    (date_value, name_value, cost_value, rate_value,
                     desc_value, ctgr_value, rmrk_value))
        
        dbc.commit()


    root = Tk()

    root.title("Add New Entry")
    root.geometry("260x380")
    root.resizable(0, 0)

    frame = Frame(root)
    
    datelb = Label(frame, text = "Date: ", font=('Consolas', 10))
    date = Entry(frame)
    namelb = Label(frame, text = "Name: ", font=('Consolas', 10))
    name = Entry(frame)
    ctgrlb = Label(frame, text = "Category: ", font=('Consolas', 10))
    ctgr = Entry(frame)
    costlb = Label(frame, text = "Cost: ", font=('Consolas', 10))
    cost = Entry(frame, width=8, justify=RIGHT)
    ratelb = Label(frame, text = "Rating:", font=('Consolas', 10))
    rate = Entry(frame, width=3, justify=CENTER)
    desclb = Label(frame, text = "Desc: ", font=('Consolas', 10))
    desc = Text(frame, height=5, width=10)
    rmrklb = Label(frame, text = "Remark: ", font=('Consolas', 10))
    rmrk = Text(frame, height=5, width=10)
    addbtn = Button(frame, text="Add", command=on_submit)

    frame.grid(column=0, row=0, sticky='n')

    datelb.grid(column=0, row=0, padx=10, pady=(13, 10), sticky='w')
    date.grid(column=1, row=0, columnspan=3, pady=(13, 10), sticky='we')
    namelb.grid(column=0, row=1, padx=10, pady=10, sticky='w')
    name.grid(column=1, row=1, columnspan=3, sticky='we')
    ctgrlb.grid(column=0, row=2, padx=10, pady=10, sticky='w')
    ctgr.grid(column=1, row=2, columnspan=3, sticky='we')
    costlb.grid(column=0, row=3, padx=10, pady=10, sticky='w')
    cost.grid(column=1, row=3, sticky='w')
    ratelb.grid(column=2, row=3, padx=10, sticky='w')
    rate.grid(column=3, row=3, sticky='w')
    desclb.grid(column=0, row=4, padx=10, pady=10, sticky='nw')
    desc.grid(column=1, row=4, columnspan=3, rowspan=2, pady=10, sticky='we')
    rmrklb.grid(column=0, row=6, padx=10, pady=10, sticky='nw')
    rmrk.grid(column=1, row=6, columnspan=3, rowspan=2, pady=10, sticky='we')
    addbtn.grid(column=1, row=8, pady=5, columnspan=2, sticky='w')

    root.mainloop()