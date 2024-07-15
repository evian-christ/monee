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

# Convert 'monthly start date' to integer
settings['month_start_date'] = int(settings['month_start_date'])

# Convert budgets to floats
budgets = [float(budget) for budget in settings['budget']]

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

    def update_stats(year, month):
    # Clear previous data
        for child in budget_table.get_children():
            budget_table.delete(child)
        for widget in budget_graph_frame.winfo_children():
            widget.destroy()

        # Calculate start date for the selected month
        if month == 0:  # Adjust for December to January transition
            start_date = datetime(year - 1, 12, settings['month_start_date'])
            end_date = datetime(year, 1, settings['month_start_date']) - timedelta(days=1)
        else:
            start_date = datetime(year, month, settings['month_start_date'])
            if month == 12:  # Adjust for January to December transition
                end_date = datetime(year + 1, 1, settings['month_start_date']) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, settings['month_start_date']) - timedelta(days=1)

        # Display current date range
        date_range_label.config(text=f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

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
            if isinstance(j, (int, float)) and j != 0:
                budget_status.append(i / j)
            else:
                budget_status.append(0)  # Handle division by zero scenario

        max_ratio = max(budget_status) if budget_status and any(budget_status) else 1  # Avoid division by zero

        for idx, (category, ratio) in enumerate(zip(name, budget_status)):
            if max_ratio != 0:
                bar_height = 300 * ratio / max_ratio  # Scale the bar height relative to the maximum ratio
            else:
                bar_height = 0

            color = "#2ecc71" if ratio <= 1 else "#e74c3c"  # Green if within budget, red if over budget

            budget_graph.create_rectangle(
                10 + 50 * idx, 400 - bar_height, 50 + 50 * idx, 400,
                fill=color, outline="black"
            )
            budget_graph.create_text(
                30 + 50 * idx, 405, text=category, anchor="n"
            )

        for i, j in zip(name, budget_status):
            budget_table.insert("", "end", values=(i, "{:.1%}".format(j)))

        budget_graph_frame.update_idletasks()
        budget_graph.configure(scrollregion=budget_graph.bbox("all"))



    def prev_month():
        # Calculate previous month and adjust year if necessary
        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year

        update_stats(prev_year, prev_month)

    def next_month():
        # Calculate next month and adjust year if necessary
        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month == 12:
            next_month = 1
            next_year = current_year + 1
        else:
            next_month = current_month + 1
            next_year = current_year

        update_stats(next_year, next_month)

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text=texts[1][lan], padding=10)

    # Display current date range
    date_range_label = Label(tab1, text="", font=("Arial", 12))
    date_range_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3)

    budget_table = Treeview(tab1, columns=("Category", "Spent"), show="headings", height=17)
    budget_table.grid(column=0, row=1, padx=20)
    budget_table.column("Category", width=130)
    budget_table.column("Spent", width=140)
    budget_table.heading("Category", text=texts[3][lan])
    budget_table.heading("Spent", text=texts[4][lan])

    budget_graph = Canvas(tab1, height=400, width=600)
    budget_graph.grid(column=1, row=1, columnspan=2)

    scrollbar = Scrollbar(tab1, orient=HORIZONTAL, command=budget_graph.xview)
    scrollbar.grid(column=1, row=2, sticky=EW, columnspan=2)
    budget_graph.configure(xscrollcommand=scrollbar.set)

    budget_graph_frame = Frame(budget_graph)
    budget_graph.create_window((0, 0), window=budget_graph_frame, anchor="nw")

    def on_canvas_configure(event):
        budget_graph.configure(scrollregion=budget_graph.bbox("all"))

    budget_graph.bind('<Configure>', on_canvas_configure)

    name = settings["category"].copy()
    budgets = settings["budget"]

    # Initially display current month's data
    update_stats(datetime.now().year, datetime.now().month)

    prev_button = Button(tab1, text="◀", command=prev_month)
    prev_button.grid(row=2, column=0, padx=10, pady=10)

    next_button = Button(tab1, text="▶", command=next_month)
    next_button.grid(row=2, column=2, padx=10, pady=10)

    tab2 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab2, text=texts[2][lan])

    notebook.grid()

    root.mainloop()
