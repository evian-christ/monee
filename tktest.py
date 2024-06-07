from tkinter import *

# main window
main = Tk()

# Title
main.title("Testing...")

# Size
main.geometry("350x200")

# Labels
lbl = Label(main, text = "Welcome!")
lbl.grid()

# function
def clicked():
    lbl.configure(text = "Thanks for clicking :)")

# button
btn = Button(main, text = "Click", command = clicked)

# set button grid
btn.grid(column = 0, row = 1)

# Execute TkInter
main.mainloop()