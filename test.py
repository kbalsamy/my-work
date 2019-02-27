# from tkinter import *


# def on_configure(event):
#     # update scrollregion after starting 'mainloop'
#     # when all widgets are in canvas
#     canvas.configure(scrollregion=canvas.bbox('all'))


# root = Tk()

# # --- create canvas with scrollbar ---

# canvas = Canvas(root)
# canvas.pack(side=LEFT, fill=BOTH, expand=1)

# scrollbar = Scrollbar(root, command=canvas.yview)
# scrollbar.pack(side=LEFT, fill='y')

# canvas.configure(yscrollcommand=scrollbar.set)

# # update scrollregion after starting 'mainloop'
# # when all widgets are in canvas
# canvas.bind('<Configure>', on_configure)

# # --- put frame in canvas ---


# def execute(frame):
#     wid = frame.winfo_children()
#     print(wid)


# frame = Frame(canvas)
# frame.pack(side=LEFT)
# canvas.create_window((250, 300), window=frame, anchor='nw', height=350, width=800)
# bf = Frame(frame)
# bf.pack()
# Button(bf, text='clear', command=lambda: execute(frame)).pack()
# for i in range(20):
#     lf = Frame(frame)
#     lf.pack(side=TOP, fill=X, expand=1)
#     for x in range(3):
#         Entry(lf, state='readonly', width=20, bd=1).pack(side=LEFT, fill=X, expand=1)

# # --- start program ---

# root.mainloop()


d = ('January2019',)

a, b = (d)

print(a)
