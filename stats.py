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
        ["Categories", "카테고리"]
    ]

    root = Toplevel()
    root.title(texts[0][lan])
    root.geometry("700x700+500+300")
    root.resizable(TRUE, TRUE) # true for now

    root.grab_set()

    notebook = Notebook(root, padding=10)


#=============================================

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text=texts[1][lan])

