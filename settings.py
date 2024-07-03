from tkinter import *
from tkinter.ttk import *
from dateAndTime import *
from tkinter import messagebox

import json
import os
import sys

#=====================================

settings = {
    "month_start_date": "1",
    "language": "English",
    "category": ["Food", "Entertainment", "Transport", "Misc"],
    "Budget": ["550", "150", "100", "100"]
}

if not os.path.exists('config.json'):
    with open('config.json', 'w') as config_file:
        json.dump(settings, config_file)
else:
    with open('config.json', 'r') as config_file:
        settings = json.load(config_file)

global lan

if settings['language'] == "English":
    lan = 0
elif settings['language'] == "한국어":
    lan = 1

#=====================================

def add_category():
    def add():
        category_value = category_entry.get()
        if category_value in settings['category']:
            messagebox.showerror("Error", "Already exists!", parent=add_window)
            pass
        else:
            category_listbox.insert(END, category_value)
            settings['category'].append(category_value)
            with open('config.json', 'w') as config_file:
                json.dump(settings, config_file)
            add_window.destroy()

    add_window = Tk()

    add_window.title("Add new category")
    add_window.geometry("260x65+1000+500")
    add_window.resizable(0, 0)

    category_entry = Entry(add_window)
    category_add = Button(add_window, text="Add", command=add)

    category_entry.grid(column=0, row=0, padx=20, pady=20)
    category_add.grid(column=1, row=0)

#=====================================

def edit_category():
    selected = category_listbox.curselection()[0]
    if not selected:
        return

    def edit():
        category_value = category_entry.get()
        if category_value in settings['category']:
            messagebox.showerror("Error", "Already exists!", parent=edit_window)
            pass
        else:
            category_listbox.delete(selected, selected)
            category_listbox.insert(END, category_value)
            settings['category'][selected] = category_value
            with open('config.json', 'w') as config_file:
                json.dump(settings, config_file)
            edit_window.destroy()

    edit_window = Tk()

    edit_window.title("Edit")
    edit_window.geometry("260x65+1000+500")
    edit_window.resizable(0, 0)

    category_entry = Entry(edit_window)
    category_entry.insert(0, settings['category'][selected])
    category_edit = Button(edit_window, text="Confirm", command=edit)

    category_entry.grid(column=0, row=0, padx=20, pady=20)
    category_edit.grid(column=1, row=0)

#=====================================

def del_category(root):
    selected = category_listbox.curselection()[0]

    confirm = messagebox.askyesno("Delete", "You sure bro?", parent=root)
    if not confirm:
        return

    category_listbox.delete(selected, selected)
    settings['category'].remove(settings['category'][selected])
    with open('config.json', 'w') as config_file:
        json.dump(settings, config_file)

#=====================================

def save_settings(day, language):
    sday = day.get()
    lang = language.get()
    settings['month_start_date'] = sday
    settings['language'] = lang
    with open('config.json', 'w') as config_file:
        json.dump(settings, config_file)

    python = sys.executable
    os.execl(python, python, * sys.argv)

#=====================================

def open_settings():
    global category_listbox

    root = Tk()

    root.title("Settings")
    root.geometry("333x333+800+300")

    notebook = Notebook(root, padding=10)
    
#=====================================

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text="General")
    startdaylb = Label(tab1, text ="Start day of month")
    startday = Combobox(
        tab1,
        width=2,
        state="readonly",
        values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    )
    startday.set(settings['month_start_date'])
    startdaylb.grid(column=0, row=0, sticky='w', padx=(20, 0))
    startday.grid(column=1, row=0, sticky='e', padx=(80, 20), pady=(40, 10))

    langlb = Label(tab1, text="Language")
    lang = Combobox(
        tab1,
        width=10,
        state="readonly",
        values=["English", "한국어"]
    )
    lang.set(settings['language'])
    langlb.grid(column=0, row=1, sticky='w', padx=(20, 0))
    lang.grid(column=1, row=1, sticky='e', padx=(80, 20), pady=(20, 10))

    btn_save = Button(tab1, text="Save", command=lambda: save_settings(startday, lang))
    btn_save.grid(column=1, row=3, sticky='e', pady=(125, 0), padx=(0, 20))

#=====================================

    tab2 = Frame(notebook, padding=(70, 30), borderwidth=2, relief="solid")
    notebook.add(tab2, text="Category")
    categorylb = Label(tab2, text="Categories: ")
    category_listbox = Listbox(tab2, selectmode=SINGLE)
    category_edit = Button(tab2, text='edit', command=edit_category)
    category_add = Button(tab2, text="+", width=5, command=add_category)
    category_del = Button(tab2, text="-", width=5, command=lambda : del_category(root))
    categorylb.grid(column=0, row=0, sticky='w', pady=5)
    category_listbox.grid(column=0, row=1, columnspan=3, sticky='nswe')
    category_edit.grid(column=0, row=2, sticky='w', pady=5)
    category_add.grid(column=1, row=2, sticky='e')
    category_del.grid(column=2, row=2, sticky='e')

    for i in settings['category']:
        category_listbox.insert(END, i)

#=====================================

    notebook.grid(sticky='nswe')

    root.mainloop()