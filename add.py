from tkinter import *
from tkinter.ttk import *

def open_add():
    root = Tk()

    root.title("Add New Entry")
    root.geometry("360x720")

    frame = Frame(root)
    
    date = Label(frame, text = "Date: ", font=('Consolas', 10))
    dateE = Entry(frame)
    name = Label(frame, text = "Name: ", font=('Consolas', 10))
    nameE = Entry(frame)
    cost = Label(frame, text = "Cost: ", font=('Consolas', 10))
    costE = Entry(frame, width=8, justify=RIGHT)
    rate = Label(frame, text = "Rating: ", font=('Consolas', 10))
    rateE = Entry(frame, width=3, justify=CENTER)

    frame.grid(column=0, row=0, sticky='n')

    date.grid(column=0, row=0, padx=10, pady=10)
    dateE.grid(column=1, row=0, columnspan=3, sticky='w')
    name.grid(column=0, row=1, padx=10, pady=10)
    nameE.grid(column=1, row=1, columnspan=3, sticky='w')
    cost.grid(column=0, row=2, padx=10, pady=10)
    costE.grid(column=1, row=2)
    rate.grid(column=2, row=2, padx=10)
    rateE.grid(column=3, row=2)

    root.mainloop()

    
