from tkinter import *
from tkinter.ttk import *
from dateAndTime import unixToStr
import sqlite3

def fetch_data():
    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()
    cursor.execute("SELECT id, date, name, category, cost, rate, desc, remark FROM expenses")
    rows = cursor.fetchall()
    dbc.close()
    return rows

def delete_selected_row():
    selected_item = table.selection()
    if not selected_item:
        return

    item = selected_item[0]
    entry_id = table.set(item, 'ID')  # Get the hidden ID

    # Connect to the database
    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (entry_id,))
    dbc.commit()
    dbc.close()

    # Remove from Treeview
    table.delete(item)

def open_view():
    global table
    root = Tk()
    root.title("View your entries")
    root.geometry("1000x700+300+200")

    frame = Frame(root, padding=15)
    frame.grid(column=0, row=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    advbtn = Button(frame, text="Advanced")
    delbtn = Button(frame, text="Delete", command=delete_selected_row)
    editbtn = Button(frame, text="Edit")
    advbtn.grid(column=1, row=0, sticky='e')
    delbtn.grid(column=0, row=2, sticky='w')
    editbtn.grid(column=1, row=2, sticky='e')

    table = Treeview(frame, columns=
                     ("ID", "Date", "Name", "Category", "Cost", "Rating", "Description", "Remark"),
                     show="headings")
    table.grid(column=0, row=1, columnspan=2, sticky='nswe', pady=10)

    table.column("ID", width=0, stretch=NO)  # Hide the ID column
    table.column("Date", width=100)
    table.column("Name", width=100)
    table.column("Category", width=100)
    table.column("Cost", width=50, anchor=E)
    table.column("Rating", width=25, anchor=CENTER)
    table.column("Description", width=200)
    table.column("Remark", width=200)

    table.heading("ID", text="ID")
    table.heading("Date", text="Date")
    table.heading("Name", text="Name")
    table.heading("Category", text="Category")
    table.heading("Cost", text="Cost")
    table.heading("Rating", text="Rating")
    table.heading("Description", text="Description")
    table.heading("Remark", text="Remark")

    rows = fetch_data()
    for row in rows:
        date_str = unixToStr(row[1])  # Convert Unix timestamp to readable date string
        # Insert data into the Treeview, including the hidden ID
        table.insert("", "end", values=(row[0], date_str, row[2], row[3], row[4], row[5], row[6], row[7]))

    root.mainloop()
