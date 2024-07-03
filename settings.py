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

    add_window = Toplevel()

    cat_texts = [
        ["New category", "새 카테고리"],
        ["Add", "추가"]
    ]

    add_window.title(cat_texts[0][lan])
    add_window.geometry("260x65+1000+500")
    add_window.resizable(0, 0)

    category_entry = Entry(add_window)
    category_add = Button(add_window, text=cat_texts[1][lan], command=add)

    category_entry.grid(column=0, row=0, padx=20, pady=20)
    category_add.grid(column=1, row=0)

    add_window.grab_set()

#=====================================

def edit_category(root):
    editexts=[
        ["Error", "오류"],
        ["Already exists!", "중복 오류"],
        ["Edit", "수정"],
        ["Confirm", "확인"],
        ["Select a category!", "수정할 카테고리를 선택하십시오"]
    ]
    
    def edit():
        category_value = category_entry.get()
        if category_value in settings['category']:
            messagebox.showerror(editexts[0][lan], editexts[1][lan], parent=edit_window)
            pass
        else:
            category_listbox.delete(selected, selected)
            category_listbox.insert(END, category_value)
            settings['category'][selected] = category_value
            with open('config.json', 'w') as config_file:
                json.dump(settings, config_file)
            edit_window.destroy()

    if category_listbox.curselection():
        selected = category_listbox.curselection()[0]

        edit_window = Toplevel()

        edit_window.title(editexts[2][lan])
        edit_window.geometry("260x65+1000+500")
        edit_window.resizable(0, 0)

        category_entry = Entry(edit_window)
        category_entry.insert(0, settings['category'][selected])
        category_edit = Button(edit_window, text=editexts[3][lan], command=edit)

        category_entry.grid(column=0, row=0, padx=20, pady=20)
        category_edit.grid(column=1, row=0)

        edit_window.grab_set()
    else:
        messagebox.showerror(editexts[0][lan], editexts[4][lan], parent=root)
        
    
    
#=====================================

def del_category(root):
    deltexts=[
        ["Delete", "삭제"],
        ["Are you sure?", "삭제하시겠습니까?"],
        ["Error", "오류"],
        ["Select a category!", "삭제할 카테고리를 선택하십시오"]
    ]

    if category_listbox.curselection():
        selected = category_listbox.curselection()[0]

        confirm = messagebox.askyesno(deltexts[0][lan], deltexts[1][lan], parent=root)
        if not confirm:
            return

        category_listbox.delete(selected, selected)
        settings['category'].remove(settings['category'][selected])
        with open('config.json', 'w') as config_file:
            json.dump(settings, config_file)
    else:
        messagebox.showerror(deltexts[2][lan], deltexts[3][lan], parent=root)
        
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
    texts=[
        ["Settings", "설정"],
        ["General", "일반"],
        ["Start day of month", "월 기준 일자"],
        ["Language", "언어"],
        ["Save", "저장"],
        ["Category", "카테고리"],
        ["Categories: ", "카테고리:"],
        ["Edit", "수정"]
    ]

    global category_listbox

    root = Toplevel()

    root.title(texts[0][lan])
    root.geometry("333x337+800+300")
    root.resizable(FALSE, FALSE)

    root.grab_set()

    notebook = Notebook(root, padding=10)
    
#=====================================

    tab1 = Frame(notebook, borderwidth=2, relief="solid")
    notebook.add(tab1, text=texts[1][lan])
    startdaylb = Label(tab1, text=texts[2][lan])
    startday = Combobox(
        tab1,
        width=2,
        state="readonly",
        values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    )
    startday.set(settings['month_start_date'])
    startdaylb.grid(column=0, row=0, sticky='w', padx=(30, 0), pady=(30, 10))
    startday.grid(column=1, row=0, sticky='e', padx=(60, 30), pady=(30, 10))

    langlb = Label(tab1, text=texts[3][lan])
    lang = Combobox(
        tab1,
        width=10,
        state="readonly",
        values=["English", "한국어"]
    )
    lang.set(settings['language'])
    langlb.grid(column=0, row=1, sticky='w', padx=(30, 0))
    lang.grid(column=1, row=1, sticky='e', padx=(60, 30), pady=(20, 10))

    btn_save = Button(tab1, text=texts[4][lan], command=lambda: save_settings(startday, lang))
    btn_save.grid(column=1, row=3, sticky='e', pady=(130, 0), padx=(0, 30))

#=====================================

    tab2 = Frame(notebook, padding=(70, 30), borderwidth=2, relief="solid")
    notebook.add(tab2, text=texts[5][lan])
    categorylb = Label(tab2, text=texts[6][lan])
    category_listbox = Listbox(tab2, selectmode=SINGLE)
    category_edit = Button(tab2, text=texts[7][lan], command=lambda: edit_category(root))
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