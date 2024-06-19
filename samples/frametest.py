
from tkinter.ttk import *
from ttkthemes import ThemedTk

root = ThemedTk(theme='yaru')

content = Frame(root)
frame = Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
namelbl = Label(content, text="Name")
name = Entry(content)


one = Checkbutton(content, text="One", onvalue=True)
two = Checkbutton(content, text="Two", onvalue=True)
three = Checkbutton(content, text="Three", onvalue=True)
ok = Button(content, text="Okay")
cancel = Button(content, text="Cancel")

content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
namelbl.grid(column=3, row=0, columnspan=2)
name.grid(column=3, row=1, columnspan=2)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.mainloop()