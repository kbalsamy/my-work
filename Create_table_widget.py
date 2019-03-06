from tkinter import *
from constants import *


class Plotter(Frame):

    def __init__(self, parent):
        Frame.__init__(self)

        self.parent = parent

        self.header_frame = Frame(self.parent)
        self.header_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.table_row = Frame(self.parent, bg='blue')
        self.table_row.pack(side=TOP, fill=BOTH, expand=1)
        self.seperator = Frame(self.parent, height=5, relief=GROOVE, bg='pink')
        self.seperator.pack(side=TOP, fill=BOTH, expand=1)
        self.banking_frame = Frame(self.parent)
        self.banking_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.charges_frame = Frame(self.parent)
        self.charges_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.create_table_gui()

    def create_table_gui(self):

        for header in headers_list:
            f1 = Frame(self.header_frame)
            f1.pack(side=LEFT, fill=BOTH, expand=1)
            f2 = Frame(f1)
            f2.pack(side=TOP, fill=BOTH, expand=1)
            Label(f2, text=header, bd=2, relief=SOLID).pack(side=TOP, fill=X, expand=1)
            if header != 'Consumer Number':
                f3 = Frame(f1)
                f3.pack(side=TOP, fill=BOTH, expand=1)

                for s in slot_list:
                    Label(f3, text=s, bd=2, relief=SOLID).pack(side=LEFT, fill=X, expand=1)
            else:
                f4 = Frame(f1)
                f4.pack(side=TOP, fill=BOTH, expand=1)
                Label(f4, text='', relief=SOLID).pack(side=LEFT, fill=X, expand=1)

    def plot_values(self, results):

        if len(results) != 3:
            Label(self.table_row, text=results, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)
        else:
            val = StringVar()
            val.set(results[0])
            Entry(self.table_row, textvariable=val, width=40, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)
            reading = results[1]
            for r in reading[0:15]:
                v = IntVar()
                v.set(r)
                Entry(self.table_row, textvariable=v, width=5, justify=CENTER, state='readonly', bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)
            self.create_banking_table()
            self.plot_bankingvalues(results)
            self.create_charges_table()
            self.plot_chargesvalues(results)

    def create_banking_table(self):
        Label(self.banking_frame, text='Banking Details').pack(side=TOP, fill=BOTH, expand=1)
        ban_head = Frame(self.banking_frame)
        ban_head.pack(side=TOP, fill=BOTH, expand=1)
        for s in slot_list:
            Label(ban_head, text=s, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)

    def plot_bankingvalues(self, values):
        ban_row = Frame(self.banking_frame)
        ban_row.pack(side=TOP, fill=BOTH, expand=1)
        readings = values[1]
        ban_readings = readings[15:]
        for val in ban_readings:
            var = IntVar()
            var.set(val)
            Entry(ban_row, textvariable=var, state='readonly', justify=CENTER, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)

    def create_charges_table(self):

        Label(self.charges_frame, text='Charges').pack(side=TOP, fill=BOTH, expand=1)
        ch_head = Frame(self.charges_frame)
        ch_head.pack(side=TOP, fill=BOTH, expand=1)
        for c in ['Code', 'Description', 'Charges']:
            Label(ch_head, text=c, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)

    def plot_chargesvalues(self, values):
        ch_row = Frame(self.charges_frame)
        ch_row.pack(side=TOP, fill=BOTH, expand=1)
        readings = values[2]
        if len(readings) > 7:
            step1 = [readings[i:i + 3] for i in range(0, len(readings), 3)]
            for ro in step1:
                row = Frame(ch_row)
                row.pack(side=TOP, fill=BOTH, expand=1)
                for val in ro:
                    var = StringVar()
                    var.set(str(val))
                    Entry(row, textvariable=var, state='readonly', justify=CENTER, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)
        else:

            for ro in readings:
                row = Frame(ch_row)
                row.pack(side=TOP, fill=BOTH, expand=1)
                for val in ro:
                    var = StringVar()
                    var.set(str(val))
                    Entry(row, textvariable=var, state='readonly', justify=CENTER, bd=2, relief=SOLID).pack(side=LEFT, fill=BOTH, expand=1)


# root = Tk()
# app = Plotter(root)
# app.plot_values(sample_results)
# app.plot_bankingvalues(sample_results)
# app.plot_chargesvalues(sample_results)
# root.mainloop()
