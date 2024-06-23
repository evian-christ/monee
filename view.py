from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
import sqlite3

def open_view():
    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()

    cursor.execute("SELECT date, name, category, cost, rate, desc, remark FROM expenses")
    rows = cursor.fetchall()

    dbc.close()

    root = Tk()

    root.title("View your entries")
    root.geometry("1000x700+300+200")

    frame = Frame(root, padding=15)

    advbtn = Button(frame, text="Advanced")
    delbtn = Button(frame, text="Delete")
    editbtn = Button(frame, text="Edit")
    table = Treeview(frame, columns=
                     ("Date", "Name", "Category", "Cost", "Rating", "Description", "Remark"),
                     show="headings")

    table.column("Date", width=1)
    table.column("Name", width=1)
    table.column("Category", width=10)
    table.column("Cost", width=1)
    table.column("Rating", width=1)
    table.column("Description")
    table.column("Remark")

    table.heading("Date", text="Date")
    table.heading("Name", text="Name")
    table.heading("Category", text="Category")
    table.heading("Cost", text="Cost")
    table.heading("Rating", text="Rating")
    table.heading("Description", text="Description")
    table.heading("Remark", text="Remark")

    frame.grid(column=0, row=0, sticky="nsew")  # Expand frame within root
    root.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    advbtn.grid(column=1, row=0, sticky='e')
    delbtn.grid(column=0, row=2, sticky='w')
    editbtn.grid(column=1, row=2, sticky='e')
    table.grid(column=0, row=1, columnspan=2, sticky='nswe', pady=10)

    for row in rows:
        date_str = unixToStr(row[0])
        table.insert("", "end", values=(date_str, row[1], row[2], row[3], row[4], row[5], row[6]))

    root.mainloop()