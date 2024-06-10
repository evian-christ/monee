from tkinter import ttk
from ttkthemes import ThemedTk

# main window
main = ThemedTk(theme='yaru')
print(main.get_themes())

# Title
main.title("Testing...")
# Size
main.geometry("350x200")

# Labels
lbl = ttk.Label(main, text = "Welcome!")
lbl.grid()

# Input field
txt = ttk.Entry(main)
txt.grid(column = 1, row = 0)

# function
def clicked():
    lbl.configure(text = txt.get())
# button
btn = ttk.Button(main, text = "Click", command = clicked)

# set button grid
btn.grid(column = 0, row = 1)

# Execute TkInter
main.mainloop()