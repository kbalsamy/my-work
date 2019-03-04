# from tkinter import *


# class testingApp(Frame):

#     def __init__(self, master):
#         Frame.__init__(self)
#         self.master = master
#         self.master.geometry('650x350')
#         self.topwidgets()
#         self.middle()
#         self.bottom()

#     def topwidgets(self):
#         frame = Frame(self.master, bg='pink')
#         frame.pack(side=TOP, fill=BOTH, expand=1)
#         Button(frame, text='add', command=lambda: print('tobe imple')).pack()
#         frame.pack_propagate(0)

#     def middle(self):
#         canvas = Canvas(self.master)
#         canvas.pack(side=TOP, fill=BOTH, expand=1)
#         canvas.pack_propagate(0)
#         scrollbar = Scrollbar(canvas, command=canvas.yview)
#         scrollbar.pack(side=RIGHT, fill='y')
#         canvas.configure(yscrollcommand=scrollbar.set)
#         frame = Frame(canvas)
#         frame.pack(side=TOP, fill=BOTH, expand=1)
#         canvas.create_window((0, 0), window=frame, anchor='nw')
#         for i in range(100):
#             lf = Frame(frame)
#             lf.pack(side=TOP, fill=X, expand=1)
#             for x in range(3):
#                 Entry(lf, state='readonly', width=20, bd=1).pack(side=LEFT, fill=X, expand=1)
#         self.master.update()
#         canvas.configure(scrollregion=canvas.bbox('all'))

#     def bottom(self):
#         frame = Frame(self.master, bg='yellow')
#         frame.pack(side=TOP, fill=BOTH, expand=1)
#         frame.pack_propagate(0)


# root = Tk()
# test = testingApp(root)
# root.mainloop()


# from selenium import webdriver

# browser = webdriver.PhantomJS()

# # browser.set_window_size(1120, 550)

# browser.get('https://www.python.org')

# print((browser.page_source).encode('utf-8'))

# # browser.quit()

# import sqlite3
# from constants import *
