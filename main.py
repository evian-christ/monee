from tkinter.ttk import *
from ttkthemes import ThemedTk
from dateAndTime import *

# main window
main = ThemedTk(theme='yaru')
main.grid_columnconfigure(0, weight=1)

# Title
main.title("monee v0.0.1")
# Size
main.geometry("1080x720")

# Date
tday = Label(main, text = today)
tday.grid()

# function
def clicked():
    # clicked

# button
btn_add = Button(main, text = "Add", command = clicked)
btn_view = Button(main, text = "View", command = clicked)
btn_settings = Button(main, text = "Settings", command = clicked)

# set button grid
btn_add.grid(column = 0, row = 2)
btn_view.grid(column = 0, row = 3)
btn_settings.grid(column = 0, row = 4)

# Execute TkInter
main.mainloop()