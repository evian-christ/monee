import sqlite3
import datetime
import time

#-------------------DB----------------------
db = sqlite3.connect('data.db')

db.execute('''
CREATE TABLE if not exists expenses
           (
           id INTEGER PRIMARY KEY,
           date INTEGER,
           desc VARCHAR(255)
           )
''')


date = datetime.date(2024, 6, 15)
desc = "McDonalds"

db.execute("INSERT INTO expenses (date, desc) VALUES (?, ?)",(time.mktime(date.timetuple()), desc))

entries = db.execute("SELECT * from expenses")

for row in entries:
    print(row)

db.commit()