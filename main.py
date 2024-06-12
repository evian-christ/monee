from tkinter.ttk import *
from ttkthemes import ThemedTk
from dateAndTime import *

# main window
main = ThemedTk(theme='yaru')
main.grid_columnconfigure(0, weight=1)

#------------------STYLE--------------------
s = Style()
s.configure('main.TButton', font = ('Consolas', 20))

# Title
main.title("monee v0.0.1")
# Size
main.geometry("1080x720")

# Date
tday = Label(main, text = today, font=('Consolas', 20), padding=20)
tday.grid()

# function
def clicked():
    pass

# button
btn_add = Button(main, text = "Add", style = 'main.TButton', padding=20, command = clicked)
btn_view = Button(main, text = "View", style = 'main.TButton', padding=10, command = clicked)
btn_settings = Button(main, text = "Settings", style = 'main.TButton', padding=10, command = clicked)

# set button grid
btn_add.grid(column = 0, row = 2, pady = 20)
btn_view.grid(column = 0, row = 3, pady = 20)
btn_settings.grid(column = 0, row = 4, pady = 20)

# Execute TkInter
main.mainloop()