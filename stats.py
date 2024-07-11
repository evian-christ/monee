from tkinter import *
from tkinter.ttk import *
from dateAndTime import *

import sqlite3
import json

with open('config.json', 'r') as config_file:
    settings = json.load(config_file)

global lan

if settings['language'] == "English":
    lan = 0
elif settings['language'] == "한국어":
    lan = 1

def open_stats():
    texts = [
        ["Statistics", "통계"],
        ["Categories", "카테고리"],
        ["Rating", "평점"],
        ["Category", "카테고리"],
        ["Spent", "소비량"]
    ]

    root = Toplevel()
    root.title(texts[0][lan])
    root.geometry("800x500+500+300")
    root.resizable(TRUE, TRUE) # true for now

    root.grab_set()

    notebook = Notebook(root, padding=20)

#=============================================

    def _on_mousewheel(event):
        if root.tk.call("tk", "windowingsystem") == "aqua":
            budget_graph.yview_scroll(-2 * (event.delta), "units")
        else:
            budget_graph.yview_scroll(-2 * (event.delta // 120), "units")

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text=texts[1][lan], padding=10)

    budget_table = Treeview(tab1, columns=("Category", "Spent"), show="headings", height=13)
    budget_table.grid(column=0, row=0, padx=20)
    budget_table.column("Category", width=190)
    budget_table.column("Spent", width=80)
    budget_table.heading("Category", text=texts[3][lan])
    budget_table.heading("Spent", text=texts[4][lan])

    budget_graph = Canvas(tab1, height=400)
    budget_graph.grid(column=1, row=0)
    
    scrollbar = Scrollbar(tab1, orient=VERTICAL, command=budget_graph.yview)
    scrollbar.grid(column=2, row=0, sticky=NS)

    budget_graph.configure(yscrollcommand=scrollbar.set)

    budget_graph_frame = Frame(budget_graph)

    budget_graph.create_window((0, 0), window=budget_graph_frame, anchor="nw")

    budget_graph.bind('<Configure>', lambda e: budget_graph.configure(scrollregion=budget_graph.bbox("all")))

    for i in range(220):
        Label(budget_graph_frame, text=f"Category {i+1}").pack()

    budget_graph.bind_all("<MouseWheel>", _on_mousewheel)

#=============================================

    tab2 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab2, text=texts[2][lan])

#=============================================

    notebook.grid()

    root.mainloop()

