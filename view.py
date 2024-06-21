from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dateAndTime import *

import sqlite3

def open_view():
    root = Tk()

    root.title("View your entries")
    root.geometry("1000x700+300+200")
    
    frame = Frame(root)

    advbtn = Button(frame, text="Advanced")
    table = Treeview(frame, columns=
                     ("Date", "Name", "Category", "Cost", "Rating", "Description", "Remark"),
                     show="headings")

    table.column("Date", width=100, stretch=NO, anchor=CENTER)
    table.column("Name", width=100, stretch=NO, anchor=CENTER)
    table.column("Category", width=100, stretch=NO)
    table.column("Cost", width=100, stretch=NO)
    table.column("Rating", width=100, stretch=NO)
    table.column("Description", width=100, stretch=NO)
    table.column("Remark", width=100, stretch=NO)

    table.column("#0", stretch=NO)
    table.column("#1", stretch=NO)

    table.heading("Date", text="Date")
    table.heading("Name", text="Name")
    table.heading("Category", text="Category")
    table.heading("Cost", text="Cost")
    table.heading("Rating", text="Rating")
    table.heading("Description", text="Description")
    table.heading("Remark", text="Remark")

    frame.grid(column=0, row=0)

    advbtn.grid(column=1, row=0, sticky='e')
    table.grid(column=0, row=1, columnspan=2, sticky='we')
    
    root.mainloop()
