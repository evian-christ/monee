from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from add import open_add
from view import open_view
from settings import open_settings, lan
from fetch import *
from proverbs import *

import random
import json
import sqlite3

dbc = sqlite3.connect('data.db')

dbc.execute('''
CREATE TABLE if not exists expenses
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER,
            name VARCHAR(32),
            cost REAL,
            rate INTEGER,
            desc VARCHAR(255),
            category VARCHAR(32),
            remark VARCHAR(255)
            )
''')

main = Tk()
main.title("m0nee v0.0.1")
main.geometry("630x210+900+400")
main.resizable("false", "false")
main.iconbitmap('icon.ico')

# Load proverbs based on language setting
if lan == 0:
    proverbs = proverbs_eng
elif lan == 1:
    proverbs = proverbs_kor

# Initialize labels and canvases
tday = Label(main, text=today, font=("Arial", 11))
tday.grid(column=0, row=0, pady=(15, 5), padx=19, sticky='w')

summary = Label(main, text=random.choice(proverbs), font=("Arial", 11))
summary.grid(column=0, row=1, pady=(6,19), padx=18, sticky='w')

bar_budget = Canvas(main, width=600, height=20)
bar_budget.grid(column=0, row=2, sticky='w', columnspan=4)

bar_time = Canvas(main, width=600, height=20)
bar_time.grid(column=0, row=3, sticky='w', columnspan=4, pady=(10, 0))

but = Frame(main)
but.grid(column=0, row=4, columnspan=4, sticky='w')

texts = [
    ["New", "추가"],
    ["View", "내역"],
    ["Stats", "통계"],
    ["Settings", "설정"]
]

btn_add = Button(but, text=texts[0][lan], command=lambda: open_add(update_ui))
btn_view = Button(but, text=texts[1][lan], command=lambda: open_view(update_ui))
btn_stats = Button(but, text=texts[2][lan], state=DISABLED)
btn_settings = Button(but, text=texts[3][lan], command=lambda: open_settings(update_ui))
btn_refresh = Button(but, text="↻", command=lambda: update_ui(), width=3)

btn_add.grid(column=0, row=4, pady=5, padx=(20, 10))
btn_view.grid(column=1, row=4, pady=25, padx=10)
btn_stats.grid(column=2, row=4, pady=5, padx=10)
btn_settings.grid(column=3, row=4, pady=5, padx=10)
btn_refresh.grid(column=4, row=4, sticky='e', padx=(180, 0))

# Function to update UI components
def update_ui():
    with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

    # Update proverbs
    summary.config(text=random.choice(proverbs))
    
    # Update budget and spending bars
    budget_total = sum(int(i) for i in settings['budget'])
    
    sday = int(settings['month_start_date'])
    if today_day < sday:  # last month - this month
        start_date = f"{sday}-{prev_month}-{prev_year}"
        end_date = f"{sday}-{otoday.month}-{otoday.year}"
    else:  # this month - next month
        start_date = f"{sday}-{otoday.month}-{otoday.year}"
        end_date = f"{sday}-{next_month}-{next_year}"
    
    cursor = dbc.cursor()
    cursor.execute('''SELECT id, date, cost
                      FROM expenses 
                      WHERE date > ? AND date < ?''',
                   (strToUnix(start_date) - 86400, strToUnix(end_date)))
    rows = cursor.fetchall()
    
    spent_total = sum(row[2] for row in rows)
    spent = spent_total * 545 / budget_total if budget_total > 0 else 0
    spent_figure = spent / 5.45 if budget_total > 0 else 0

    tspent = 545 * (otoday.timestamp() - strToUnix(start_date)) / (strToUnix(end_date) - strToUnix(start_date))

    def bar_x(i):
        output = i
        if output > 545:
            output = 545
        return output
    
    def text_x(i):
        output = i
        if output > 500:
            output = 500
        return output+7

    bar_budget.delete("all")
    bar_budget.create_text(30, 12, fill="black", text="£", font=('Arial 13 bold'))
    bar_budget.create_rectangle(55, 5, 600, 20, fill='white')
    bar_budget.create_rectangle(55, 5, 55+bar_x(spent), 20, fill='grey')
    bar_budget.create_text(55+text_x(spent), 12, fill="black", text=f'{spent_figure:.1f}%', anchor='w')

    bar_time.delete("all")
    bar_time.create_text(30, 15, fill="black", text="🕓", font=('10'))
    bar_time.create_rectangle(55, 5, 600, 20, fill='white')
    bar_time.create_rectangle(55, 5, 55+bar_x(tspent), 20, fill='grey')
    bar_time.create_text(55+text_x(tspent), 12, fill="black", text=f'{tspent / 5.45:.1f}%', anchor='w')

update_ui()  # Initial UI update

main.grab_set()
main.mainloop()
