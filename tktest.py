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

# Labels
lbl = Label(main, text = today)
lbl.grid(sticky='')

# Input field
txt = Entry(main)
txt.grid(column = 0, row = 1)

# function
def clicked():
    lbl.configure(text = txt.get())
# button
btn = Button(main, text = "Click", command = clicked)

# set button grid
btn.grid(column = 0, row = 2)

# Execute TkInter
main.mainloop()