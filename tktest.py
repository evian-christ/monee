from tkinter import *

# main window
main = Tk()

# Title
main.title("Testing...")
# Size
main.geometry("350x200")


# Menu bar
menu = Menu(main)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
main.config(menu=menu)

# Labels
lbl = Label(main, text = "Welcome!")
lbl.grid()

# Input field
txt = Entry(main)
txt.grid(column = 1, row = 0)

# function
def clicked():
    lbl.configure(text = txt.get())
# button
btn = Button(main, text = "Click", command = clicked)

# set button grid
btn.grid(column = 0, row = 1)

# Execute TkInter
main.mainloop()