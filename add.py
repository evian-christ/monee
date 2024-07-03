from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from dateAndTime import *
from settings import lan

import sqlite3
import json

def open_add():
    with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

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

            dbc.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                        (date_value, name_value, cost_value, rate_value,
                        desc_value, ctgr_value, rmrk_value))
            
            dbc.commit()
            dbc.close()

            root.destroy()
            print("added succesfully!")
        
        except Exception as e:
            messagebox.showerror("Error", e)

    texts = [
        ["New expense", "새로운 지출"],
        ["Date: ", "날짜: "],
        ["Label: ", "레이블: "],
        ["Category: ", "카테고리: "],
        ["Cost: ", "비용: "],
        ["Rating: ", "평점: "],
        ["Desc: ", "상세: "],
        ["Remark: ", "비고: "],
        ["Add", "추가"]
    ]

    root = Tk()

    root.title(texts[0][lan])
    root.geometry("260x380+900+350")
    root.resizable(0, 0)

    frame = Frame(root)
    
    datelb = Label(frame, text=texts[1][lan], font=('Consolas', 10))
    date = Entry(frame)
    date.insert(0, today)
    namelb = Label(frame, text=texts[2][lan], font=('Consolas', 10))
    name = Entry(frame)
    ctgrlb = Label(frame, text=texts[3][lan], font=('Consolas', 10))
    ctgr = Combobox(
        frame,
        state="readonly",
        values=settings['category']
    )
    costlb = Label(frame, text=texts[4][lan], font=('Consolas', 10))
    cost = Entry(frame, width=6, justify=RIGHT)
    ratelb = Label(frame, text=texts[5][lan], font=('Consolas', 10))
    rate = Combobox(
        frame,
        width=2,
        state="readonly",
        values=[5,4,3,2,1]
    )
    desclb = Label(frame, text=texts[6][lan], font=('Consolas', 10))
    desc = Text(frame, height=5, width=10)
    rmrklb = Label(frame, text=texts[7][lan], font=('Consolas', 10))
    rmrk = Text(frame, height=5, width=10)
    addbtn = Button(frame, text=texts[8][lan], command=on_submit)

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