from tkinter import *
from tkinter.ttk import *

def open_add():
    root = Tk()

    root.title("Add New Entry")
    root.geometry("260x340")

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
    desc = Text(frame, height=5, width=15)
    rmrklb = Label(frame, text = "Remark: ", font=('Consolas', 10))
    rmrk = Text(frame, height=5, width=15)

    frame.grid(column=0, row=0, sticky='n')

    datelb.grid(column=0, row=0, padx=10, pady=10, sticky='w')
    date.grid(column=1, row=0, columnspan=3, sticky='we')
    namelb.grid(column=0, row=1, padx=10, pady=10, sticky='w')
    name.grid(column=1, row=1, columnspan=3, sticky='we')
    ctgrlb.grid(column=0, row=2, padx=10, pady=10, sticky='w')
    ctgr.grid(column=1, row=2, columnspan=3, sticky='we')
    costlb.grid(column=0, row=3, padx=10, pady=10, sticky='w')
    cost.grid(column=1, row=3)
    ratelb.grid(column=2, row=3, padx=10, sticky='w')
    rate.grid(column=3, row=3, sticky='w')
    desclb.grid(column=0, row=4, padx=10, pady=10, sticky='nw')
    desc.grid(column=1, row=4, columnspan=3, rowspan=2, pady=10, sticky='we')
    rmrklb.grid(column=0, row=6, padx=10, pady=10, sticky='nw')
    rmrk.grid(column=1, row=6, columnspan=3, rowspan=2, pady=10, sticky='we')


    root.mainloop()

    
