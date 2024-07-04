from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from add import open_add
from view import open_view
from settings import open_settings, lan
from fetch import *

import random
import json
import sqlite3

with open('config.json', 'r') as config_file:
    settings = json.load(config_file)

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

#=====================================

main = Tk()

main.title("m0nee v0.0.1")
main.geometry("630x210+900+400")

#=====================================

if lan == 1 or lan == 0:
    with open("proverbs_kor.txt", "r", encoding='utf-8') as f:
        proverbs = (f.read()).split("\n")
elif lan == 0:
    with open("proverbs_eng.txt", "r", encoding='utf-8') as f:
        proverbs = (f.read()).split("\n")

tday = Label(main, text=today)
tday.grid(column=0, row=0, pady=(15, 5), padx=20, sticky='w')
summary = Label(main, text=random.choice(proverbs), font=("Arial", 11))
summary.grid(column=0, row=1, pady=(6,19), padx=18, sticky='w')

#-----------------------------------------

budget_total = 0
for i in settings['budget']:
    budget_total += int(i)

sday = int(settings['month_start_date'])
if today_day < sday: # last month - this month
    start_date=str(sday)+"-"+str(prev_month)+"-"+str(prev_year)
    end_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
else: # this month - next month
    start_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
    end_date=str(sday)+"-"+str(next_month)+"-"+str(next_year)

dbc = sqlite3.connect('data.db')
cursor = dbc.cursor()
cursor.execute('''SELECT id, date, cost
            FROM expenses 
            WHERE date > ? AND date < ?''',
            (strToUnix(start_date)-86400, strToUnix(end_date)))
rows = cursor.fetchall()
dbc.close()

spent_total = 0
for row in rows:
    spent_total += row[2]

if budget_total > 0:
    spent = spent_total*600/budget_total
else:
    spent = 100

#------------------------------------------

sday = int(settings['month_start_date'])
if today_day < sday: # last month - this month
    start_date=str(sday)+"-"+str(prev_month)+"-"+str(prev_year)
    end_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
else: # this month - next month
    start_date=str(sday)+"-"+str(otoday.month)+"-"+str(otoday.year)
    end_date=str(sday)+"-"+str(next_month)+"-"+str(next_year)

tspent = 600*(otoday.timestamp()-strToUnix(start_date))/(strToUnix(end_date)-strToUnix(start_date))

#------------------------------------------

bar_budget = Canvas(main, width=600, height=20)
bar_budget.grid(column=0, row=2, sticky='w', columnspan=4)
bar_budget.create_text(30,12,fill="black",text="£", font=('Arial 13 bold'))
bar_budget.create_rectangle(55,5,600,20, fill='white')
bar_budget.create_rectangle(55,5,spent,20, fill='grey')
bar_budget.create_text(spent+5 if spent < 560 else 565,12,fill="black",text=f'{spent/6:.1f}'+"%",anchor='w')

bar_time = Canvas(main, width=600, height=20)
bar_time.grid(column=0, row=3, sticky='w', columnspan=4, pady=(10, 0))
bar_time.create_text(30,15,fill="black",text="🕓", font=('10'))
bar_time.create_rectangle(55,5,600,20, fill='white')
bar_time.create_rectangle(55,5,tspent,20, fill='grey')
bar_time.create_text(tspent+5 if tspent < 560 else 565,12,fill="black",text=f'{tspent/6:.1f}'+"%",anchor='w')


but = Frame(main)
but.grid(column=0, row=4, columnspan=4, sticky='w')

texts = [
    ["New", "추가"],
    ["View", "내역"],
    ["Stats", "통계"],
    ["Settings", "설정"]
]

btn_add = Button(but, text = texts[0][lan], command = open_add)
btn_view = Button(but, text = texts[1][lan], command = open_view)
btn_stats = Button(but, text = texts[2][lan], state=DISABLED)
btn_settings = Button(but, text = texts[3][lan], command = open_settings)

btn_add.grid(column=0, row=4, pady=5, padx=(20, 10))
btn_view.grid(column=1, row=4, pady=25, padx=10)
btn_stats.grid(column=2, row=4, pady=5, padx=10)
btn_settings.grid(column=3, row=4, pady=5, padx=10)

main.mainloop()