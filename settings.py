from tkinter import *
from tkinter.ttk import *
from dateAndTime import *

import json
import os

def open_settings():
    root = Tk()

    root.title("Settings")
    root.geometry("500x500+800+300")

    notebook = Notebook(root, padding=10)

    tab1 = Frame(notebook, padding=50)
    notebook.add(tab1, text="General")
    frame1 = Frame(tab1)
    startdaylb = Label(frame1, text = "Start day of month: ", font=('Consolas', 10))
    startday = Combobox(
        frame1,
        width=2,
        state="readonly",
        values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    )
    startdaylb.grid(column=0, row=0)
    startday.grid(column=1, row=0)
    
    frame1.grid(column=0, row=0, sticky='nswe')

    notebook.grid(sticky='nswe')

    root.mainloop()