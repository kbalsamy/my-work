from tkinter import *


class Table_creator(Frame):

    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.is_row = False
        self.pack(fill=X)
        self.header = Frame(self)
        self.header.pack(side=TOP, fill=BOTH, expand=1)
        self.row = Frame(self)
        self.row.pack(side=TOP, fill=BOTH, expand=1)

    def exim_table(self, name, single_header=True):

        if single_header:
            h = Frame(self.header, relief=SOLID, bd=1, bg='#a0beef')
            h.pack(side=LEFT, fill=BOTH, expand=1)
            Label(h, text=name, height=2, bg='#a0beef').pack()
        else:
            exim_frame = Frame(self.header, relief=SOLID, bd=1, bg='#a0beef')
            exim_frame.pack(side=LEFT, fill=BOTH, expand=1)
            Label(exim_frame, text=name, bg='#a0beef').pack()
            con_frame = Frame(exim_frame, relief=SOLID, bd=0, bg='#a0beef')
            con_frame.pack(side=TOP, fill=BOTH, expand=1)
            c = ['C1', 'C2', 'C3', 'C4', 'C5']
            for i in c:
                Label(con_frame, text=i, bd=1, relief=SOLID, bg='#a0beef').pack(side=LEFT, fill=BOTH, expand=1)

    def add_row(self, values):

        if len(values) > 2:
            status = StringVar()
            status.set(values)
            Entry(self.row, textvariable=status, state='readonly', bd=1, relief=SOLID, width=32).pack(side=LEFT, fill=BOTH, expand=1)
            # Frame(self.row, height=140, bg='red').pack(side=TOP, fill=Y)

        else:
            s = StringVar()
            s.set(values[0])
            Entry(self.row, textvariable=s, state='readonly', bd=1, relief=SOLID, width=40).pack(side=LEFT, fill=BOTH, expand=1)
            for val in values[1]:
                v = IntVar()
                v.set(val)
                Entry(self.row, textvariable=v, state='readonly', bd=1, relief=SOLID, width=5).pack(side=LEFT, fill=BOTH, expand=1)
            self.is_row = True
            Frame(self.window, height=400).pack(side=TOP, fill=Y)
