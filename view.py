from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from tkinter import messagebox
from decimal import Decimal
from add import texts as addtext
from settings import lan
from fetch import *

import sqlite3
import json
import numbers

global page
page = 0

with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

def fetch_data():
    sday = int(settings['month_start_date'])
    if today_day < sday: # last month - this month
        start_date=str(sday-1)+"-"+str(prev_month)+"-"+str(prev_year)
        end_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
    else: # this month - next month
        start_date=str(sday-1)+"-"+str(otoday.month)+"-"+str(otoday.year)
        end_date=str(sday)+"-"+str(next_month)+"-"+str(next_year)

    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()
    cursor.execute('''SELECT id, date, name, category, cost, rate, desc, remark
                   FROM expenses 
                   WHERE date > ? AND date < ?
                    ORDER BY date DESC''',
                   (strToUnix(start_date), strToUnix(end_date)))
    rows = cursor.fetchall()
    dbc.close()
    return rows

def fetch_prev_month(direction):
    global page
    page += direction

    for item in table.get_children():
        table.delete(item)

    sday = int(settings['month_start_date'])
    if today_day < sday: # last month - this month
        start_date=str(sday-1)+"-"+str(prev_month)+"-"+str(prev_year)
        end_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
    else: # this month - next month
        start_date=str(sday-1)+"-"+str(otoday.month)+"-"+str(otoday.year)
        end_date=str(sday)+"-"+str(next_month)+"-"+str(next_year)

    start_date = adjust_date(start_date, page)
    end_date = adjust_date(end_date, page)

    dbc = sqlite3.connect('data.db')
    cursor = dbc.cursor()
    cursor.execute('''SELECT id, date, name, category, cost, rate, desc, remark
                   FROM expenses 
                   WHERE date > ? AND date < ?
                    ORDER BY date DESC''',
                   (strToUnix(start_date), strToUnix(end_date)))
    rows = cursor.fetchall()
    dbc.close()

    for row in rows:
        date_str = unixToStr(row[1])
        if isinstance(row[4], numbers.Number):
            cost = Decimal(row[4]).quantize(Decimal('0.01'))
        else:
            cost = row[4]
        table.insert("", "end", values=(row[0], date_str, row[2], row[3], cost, row[5], row[6], row[7]))
    

def open_add(oroot):
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
            c = dbc.cursor()

            c.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                        (date_value, name_value, cost_value, rate_value,
                        desc_value, ctgr_value, rmrk_value))
            
            dbc.commit()
            print(c.lastrowid)
            dbc.close()

            date_str = unixToStr(date_value)
            table.insert("", "0", values=(c.lastrowid, date_str, name_value, ctgr_value, cost_value, rate_value, desc_value, rmrk_value))

            on_closing()
        except Exception as e:
            messagebox.showerror("Error", e, parent=root)

    root = Toplevel()

    root.title(addtext[0][lan])
    root.geometry("260x380+900+350")
    root.resizable(0, 0)

    root.grab_set()

    frame = Frame(root)
    
    datelb = Label(frame, text=addtext[1][lan], font=('Consolas', 10))
    date = Entry(frame)
    date.insert(0, today)
    namelb = Label(frame, text=addtext[2][lan], font=('Consolas', 10))
    name = Entry(frame)
    ctgrlb = Label(frame, text=addtext[3][lan], font=('Consolas', 10))
    ctgr = Combobox(
        frame,
        state="readonly",
        values=settings['category']
    )
    costlb = Label(frame, text=addtext[4][lan], font=('Consolas', 10))
    cost = Entry(frame, width=6, justify=RIGHT)
    ratelb = Label(frame, text=addtext[5][lan], font=('Consolas', 10))
    rate = Combobox(
        frame,
        width=2,
        state="readonly",
        values=[5,4,3,2,1]
    )
    desclb = Label(frame, text=addtext[6][lan], font=('Consolas', 10))
    desc = Text(frame, height=5, width=10)
    rmrklb = Label(frame, text=addtext[7][lan], font=('Consolas', 10))
    rmrk = Text(frame, height=5, width=10)
    addbtn = Button(frame, text=addtext[8][lan], command=on_submit)

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

    def on_closing():
        oroot.grab_set()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

def delete_selected_row(root):
    
    if table.selection():
        selected_item = table.selection()

        item = selected_item[0]
        entry_id = table.set(item, 'ID')  # Get the hidden ID

        confirmlb = ["You sure bro?", "삭제하시겠습니까????"]

        confirm = messagebox.askyesno("Delete", confirmlb[lan], parent=root)
        if not confirm:
            return

        # Connect to the database
        dbc = sqlite3.connect('data.db')
        cursor = dbc.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (entry_id,))
        dbc.commit()
        dbc.close()

        # Remove from Treeview
        table.delete(item)
    else:
        deltexts=[
            ["Error", "오류"],
            ["Select an item!", "삭제할 항목을 선택하십시오"]
        ]
        messagebox.showerror(deltexts[0][lan], deltexts[1][lan], parent=root)

def edit_selected_row(oroot, settings):
    edittext=[
        ["Edit ", "수정 "],
        ["Save", "저장"],
        ["Error", "오류"],
        ["Select an item!", "수정할 항목을 선택하십시오"]
    ]
    
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

            on_closing()
        
        except Exception as e:
            messagebox.showerror("Error", e)
    
    
    if table.selection():
        selected_item = table.selection()
    
        item = selected_item[0]
        entry_id = table.set(item, 'ID')  # Get the hidden ID

        # Connect to the database
        dbc = sqlite3.connect('data.db')
        cursor = dbc.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id=?", (entry_id,))
        dbc.commit()
        entry = cursor.fetchone()
        dbc.close()

        root = Toplevel()

        root.title(edittext[0][lan] + str(entry[0]))
        root.geometry("260x380+900+350")
        root.resizable(0, 0)
        root.grab_set()

        frame = Frame(root)
        
        datelb = Label(frame, text=addtext[1][lan], font=('Consolas', 10))
        date = Entry(frame)
        date.insert(0, unixToStr(entry[1]))
        namelb = Label(frame, text=addtext[2][lan], font=('Consolas', 10))
        name = Entry(frame)
        name.insert(0, entry[2])
        ctgrlb = Label(frame, text=addtext[3][lan], font=('Consolas', 10))
        ctgr = Combobox(
            frame,
            state="readonly",
            values=settings['category']
        )
        ctgr.set(entry[6])
        costlb = Label(frame, text=addtext[4][lan], font=('Consolas', 10))
        cost = Entry(frame, width=6, justify=RIGHT)
        cost.insert(0, entry[3])
        ratelb = Label(frame, text=addtext[5][lan], font=('Consolas', 10))
        rate = Combobox(
            frame,
            width=2,
            state="readonly",
            values=[5,4,3,2,1]
        )
        rate.set(entry[4])
        desclb = Label(frame, text=addtext[6][lan], font=('Consolas', 10))
        desc = Text(frame, height=5, width=10)
        desc.insert("1.0", entry[5])
        rmrklb = Label(frame, text=addtext[7][lan], font=('Consolas', 10))
        rmrk = Text(frame, height=5, width=10)
        rmrk.insert("1.0", entry[7])
        editbtn = Button(frame, text=edittext[1][lan], command=on_submit)

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

        def on_closing():
            oroot.grab_set()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
    else:
        messagebox.showerror(edittext[2][lan], edittext[3][lan], parent=oroot)

def open_view():
    with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

    texts=[
        ["View your expense history", "지출 내역"],
        ["Advanced", "고급"],
        ["Delete", "삭제"],
        ["Edit", "수정"],
        ["Add", "추가"],
        ["Date", "날짜"],
        ["Label", "레이블"],
        ["Category", "카테고리"],
        ["Cost", "비용"],
        ["Rating", "평점"],
        ["Description", "상세"],
        ["Remark", "비고"]
    ]

    global table
    root = Toplevel()
    root.title(texts[0][lan])
    root.geometry("1000x390+300+200")
    root.grab_set()

    frame = Frame(root, padding=15)
    frame.grid(column=0, row=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    btn_advc = Button(frame, text=texts[1][lan], state="disabled") # feature not implemented yet
    btn_del = Button(frame, text=texts[2][lan], command=lambda: delete_selected_row(root))
    btn_edit = Button(frame, text=texts[3][lan], command=lambda: edit_selected_row(root, settings))
    btn_add = Button(frame, text=texts[4][lan], command=lambda: open_add(root))
    btn_advc.grid(column=1, row=0, sticky='e')
    btn_del.grid(column=1, row=2, sticky='e')
    btn_edit.grid(column=1, row=2, sticky='e', padx=(10, 90))
    btn_add.grid(column=1, row=2, sticky='e', padx=(0, 180))

    btn_prev = Button(frame, text="<", width=4, command=lambda: fetch_prev_month(-1))
    btn_next = Button(frame, text=">", width=4, command=lambda: fetch_prev_month(1))
    btn_prev.grid(column=0, row=0, sticky='w', padx=(10, 0))
    btn_next.grid(column=0, row=0, sticky='w', padx=(55, 0))

    lbl_cur = Label(frame, text="Current Month", font=(30))
    lbl_cur.grid(column=0, row=0, sticky='w', padx=(100, 0))

    table = Treeview(frame, columns=
                     ("ID", "Date", "Name", "Category", "Cost", "Rating", "Description", "Remark"),
                     show="headings")
    table.grid(column=0, row=1, columnspan=2, sticky='nswe', pady=10, padx=(10, 0))

    scrollbar = Scrollbar(frame, orient=VERTICAL, command=table.yview)
    scrollbar.grid(column=2, row=1, sticky='nse')

    table.configure(yscrollcommand=scrollbar.set)

    table.column("ID", width=0, stretch=NO)  # Hide the ID column
    table.column("Date", width=100)
    table.column("Name", width=100)
    table.column("Category", width=100)
    table.column("Cost", width=50, anchor=E)
    table.column("Rating", width=25, anchor=CENTER)
    table.column("Description", width=200)
    table.column("Remark", width=200)

    table.heading("ID", text="ID")
    table.heading("Date", text=texts[5][lan])
    table.heading("Name", text=texts[6][lan])
    table.heading("Category", text=texts[7][lan])
    table.heading("Cost", text=texts[8][lan])
    table.heading("Rating", text=texts[9][lan])
    table.heading("Description", text=texts[10][lan])
    table.heading("Remark", text=texts[11][lan])

    rows = fetch_data()
    for row in rows:
        date_str = unixToStr(row[1])
        if isinstance(row[4], numbers.Number):
            cost = Decimal(row[4]).quantize(Decimal('0.01'))
        else:
            cost = row[4]
        table.insert("", "end", values=(row[0], date_str, row[2], row[3], cost, row[5], row[6], row[7]))

    root.mainloop()
