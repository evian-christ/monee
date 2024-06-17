from tkinter.ttk import *
from ttkthemes import ThemedTk
from dateAndTime import *

#----------------main window----------------
main = ThemedTk(theme='yaru')
main.grid_columnconfigure(0, weight=1)

#------------------STYLE--------------------
s = Style()
s.configure('main.TButton', font = ('Consolas', 20))

#------------------Title--------------------
main.title("monee v0.0.1")
#-------------------Size--------------------
main.geometry("250x305")

#-------------------Date--------------------
tday = Label(main, text = today, font=('Consolas', 20))
tday.grid(pady=7, sticky='n')

#-----------------function------------------
def open_add():
    addWindow = ThemedTk(theme='yaru')

    addWindow.title("Add New Entry")

    addWindow.geometry("720x360")

def open_view():
    viewWindow = ThemedTk(theme='yaru')

    viewWindow.title("View history")

    viewWindow.geometry("1080x720")

#------------------button--------------------
btn_add = Button(main, text = "Add", style = 'main.TButton', padding=10, command = open_add)
btn_view = Button(main, text = "View", style = 'main.TButton', padding=10, command = open_view)
btn_settings = Button(main, text = "Settings", style = 'main.TButton', padding=10, command = open_add)

#--------------set button grid---------------
btn_add.grid(column = 0, row = 2, pady = 10)
btn_view.grid(column = 0, row = 3, pady = 10)
btn_settings.grid(column = 0, row = 4, pady = 10)

#---------------Execute TkInter--------------
main.mainloop()