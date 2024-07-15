from tkinter import *
from tkinter.ttk import *
import json
import sqlite3
from datetime import datetime, timedelta

dbc = sqlite3.connect('data.db')
cursor = dbc.cursor()

# Load settings
with open('config.json', 'r') as config_file:
    settings = json.load(config_file)

lan = 0 if settings['language'] == "English" else 1

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
    root.resizable(True, True)
    root.grab_set()

    notebook = Notebook(root, padding=20)

    def _on_mousewheel(event):
        if root.tk.call("tk", "windowingsystem") == "aqua":
            budget_graph.yview_scroll(-2 * (event.delta), "units")
        else:
            budget_graph.yview_scroll(-1 * (event.delta // 120), "units")

    def update_stats():
        # Clear previous data
        for child in budget_table.get_children():
            budget_table.delete(child)
        for widget in budget_graph_frame.winfo_children():
            widget.destroy()

        # Calculate current month and year based on monthly start date
        today = datetime.today()
        if today.day < int(settings['month_start_date']):
            # Last month
            start_date = today.replace(day=int(settings['month_start_date'])) - timedelta(days=int(settings['month_start_date']))
            end_date = today.replace(day=int(settings['month_start_date'])) - timedelta(days=1)
        else:
            # This month
            start_date = today.replace(day=int(settings['month_start_date']))
            end_date = today.replace(day=int(settings['month_start_date'])) + timedelta(days=int(settings['month_start_date']) - 1)
        
        cursor.execute('''
            SELECT category, SUM(cost) AS total_spent
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY category
        ''', (int(start_date.timestamp()), int(end_date.timestamp())))

        category_sums = {}
        for row in cursor.fetchall():
            category = row[0]
            total_spent = row[1]
            category_sums[category] = total_spent

        ordered_dict = {key: category_sums.get(key, 0) for key in name}

        budget_status = []

        for i, j in zip(list(ordered_dict.values()), budgets):
            budget_status.append("{:.0f}".format(i) + "/" + str(j))

        for i, j in zip(name, budget_status):
            budget_table.insert("", "end", values=(i, j))

        for i in name:
            temp = Frame(budget_graph_frame, padding=10, borderwidth=1, relief="raised")
            temp.pack(fill=BOTH)
            Label(temp, text=i).pack(side=LEFT)

        budget_graph_frame.update_idletasks()
        budget_graph.configure(scrollregion=budget_graph.bbox("all"))

    def prev_month():
        # Adjust monthly start date and update
        temp = int(settings['month_start_date']) - 1
        settings['month_start_date'] = str(temp)
        update_stats()

    def next_month():
        # Adjust monthly start date and update
        temp = int(settings['month_start_date']) + 1
        settings['month_start_date'] = str(temp)
        update_stats()

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text=texts[1][lan], padding=10)

    budget_table = Treeview(tab1, columns=("Category", "Spent"), show="headings", height=17)
    budget_table.grid(column=0, row=1, padx=20)
    budget_table.column("Category", width=130)
    budget_table.column("Spent", width=140)
    budget_table.heading("Category", text=texts[3][lan])
    budget_table.heading("Spent", text=texts[4][lan])

    budget_graph = Canvas(tab1, height=400, width=200)
    budget_graph.grid(column=1, row=1)

    scrollbar = Scrollbar(tab1, orient=VERTICAL, command=budget_graph.yview)
    scrollbar.grid(column=2, row=1, sticky=NS)

    budget_graph.configure(yscrollcommand=scrollbar.set)

    budget_graph_frame = Frame(budget_graph)
    budget_graph.create_window((0, 0), window=budget_graph_frame, anchor="nw")

    def on_canvas_configure(event):
        budget_graph.configure(scrollregion=budget_graph.bbox("all"))

    budget_graph.bind('<Configure>', on_canvas_configure)

    name = settings["category"].copy()
    budgets = settings["budget"]

    update_stats()

    prev_button = Button(root, text="◀", command=prev_month)
    prev_button.grid(row=0, column=0, padx=10, pady=10)

    next_button = Button(root, text="▶", command=next_month)
    next_button.grid(row=0, column=1, padx=10, pady=10)

    tab2 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab2, text=texts[2][lan])

    notebook.grid()

    root.mainloop()
