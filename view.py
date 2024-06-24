from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from tkinter import messagebox
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

def edit_selected_row():
    def on_submit():
        try:
            date_value = strToUnix(date.get())
            name_value = name.get()
            ctgr_value = ctgr.get()
            cost_value = cost.get()
            rate_value = rate.get()
            desc_value = desc.get("1.0", END).strip()
            rmrk_value = rmrk.get("1.0", END).strip()

            dbc = sqlite3.connect('data.db')

            dbc.execute("UPDATE expenses SET date=?, name=?, category=?, cost=?, rate=?, desc=?, remark=? WHERE id=?",
                        (date_value, name_value, ctgr_value, cost_value,
                        rate_value, desc_value, rmrk_value, entry_id))
            
            dbc.commit()
            dbc.close()

            selected_item = table.selection()
            if selected_item:
                item = selected_item[0]
                table.item(item, values=(entry_id, unixToStr(date_value), name_value, ctgr_value,
                                         cost_value, rate_value, desc_value, rmrk_value))

            root.destroy()
            print("edited succesfully!")
        
        except Exception as e:
            messagebox.showerror("Error", e)
    
    selected_item = table.selection()
    if not selected_item:
        return
    
    item = selected_item[0]
    entry_id = table.set(item, 'ID')  # Get the hidden ID

    # Connect to the database
    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (entry_id,))
    dbc.commit()
    entry = cursor.fetchone()
    dbc.close()

    root = Tk()

    root.title("Edit " + str(entry[0]))
    root.geometry("260x380+900+350")
    root.resizable(0, 0)

    frame = Frame(root)
    
    datelb = Label(frame, text = "Date: ", font=('Consolas', 10))
    date = Entry(frame)
    date.insert(0, unixToStr(entry[1]))
    namelb = Label(frame, text = "Name: ", font=('Consolas', 10))
    name = Entry(frame)
    name.insert(0, entry[2])
    ctgrlb = Label(frame, text = "Category: ", font=('Consolas', 10))
    ctgr = Combobox(
        frame,
        state="readonly",
        values=["Food", "Entertainment", "Transport", "Misc"]
    )
    ctgr.set(entry[6])
    costlb = Label(frame, text = "Cost: ", font=('Consolas', 10))
    cost = Entry(frame, width=6, justify=RIGHT)
    cost.insert(0, entry[3])
    ratelb = Label(frame, text = "Rating:", font=('Consolas', 10))
    rate = Combobox(
        frame,
        width=2,
        state="readonly",
        values=[5,4,3,2,1]
    )
    rate.set(entry[4])
    desclb = Label(frame, text = "Desc: ", font=('Consolas', 10))
    desc = Text(frame, height=5, width=10)
    desc.insert("1.0", entry[5])
    rmrklb = Label(frame, text = "Remark: ", font=('Consolas', 10))
    rmrk = Text(frame, height=5, width=10)
    rmrk.insert("1.0", entry[7])
    editbtn = Button(frame, text="Save", command=on_submit)

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
    editbtn.grid(column=1, row=8, pady=5, columnspan=2, sticky='w')

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
    editbtn = Button(frame, text="Edit", command=edit_selected_row)
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
