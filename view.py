from tkinter import *
from tkinter.ttk import *
import sqlite3

def open_view():
    root = Tk()

    root.title("View your entries")
    root.geometry("1000x700+300+200")

    frame = Frame(root, padding=15)

    advbtn = Button(frame, text="Advanced")
    table = Treeview(frame, columns=
                     ("Date", "Name", "Category", "Cost", "Rating", "Description", "Remark"),
                     show="headings")

    table.heading("Date", text="Date")
    table.heading("Name", text="Name")
    table.heading("Category", text="Category")
    table.heading("Cost", text="Cost")
    table.heading("Rating", text="Rating")
    table.heading("Description", text="Description")
    table.heading("Remark", text="Remark")

    frame.grid(column=0, row=0, sticky="nsew")  # Expand frame within root
    root.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)  # Expand column 0 of root
    frame.columnconfigure(1, weight=1)  # Expand column 0 of root

    advbtn.grid(column=1, row=0, sticky='e')
    table.grid(column=0, row=1, columnspan=2, sticky='nswe')

    root.mainloop()