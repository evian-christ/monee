import sqlite3

#-------------------DB----------------------
db = sqlite3.connect('data.db')

db.execute('''
CREATE TABLE if not exists expenses
           (
           id INTEGER,
           date INTEGER,
           desc VARCHAR(255)
           )
''')