from tkinter import *
from constants import *
import file_creator as excel
import Pmw
import logging


class databaseFrame(Frame):

    def __init__(self, master, display):
        Frame.__init__(self)
        self.master = master
        self.display = display
        self.consumer = StringVar()
        self.month = StringVar()
        self.year = IntVar()
        self.tablename = StringVar()

        # self.pack(side=TOP, fill=BOTH, expand=1)
        self.av_db = excel.get_table_name()
        # logging.info('Available data {}'.format(self.av_db[0]))
        search_pane = Frame(self.master, bd=3, relief=GROOVE)
        search_pane.pack(side=TOP, fill=BOTH, expand=1)
        Label(search_pane, text='Search Database here', anchor='w').pack(side=TOP, fill=X, expand=1)
        Label(search_pane, text='Select available Database here', anchor='w').pack(side=LEFT)
        OptionMenu(search_pane, self.tablename, *self.av_db).pack(side=LEFT, anchor='w')
        # unpack the av_db
        if not self.av_db[0] == 'Not available':
            btn1 = Button(search_pane, text='Display', state='active', command=self.show_db_table)
            btn1.pack(side=LEFT)
        else:
            btn1 = Button(search_pane, text='Display', state=DISABLED, command=self.show_db_table)
            btn1.pack(side=LEFT)
        btn2 = Button(search_pane, text='Clear', command=self.clear_display)
        btn2.pack(side=LEFT)

        search_pane2 = Frame(self.master, bd=5, relief=GROOVE)
        search_pane2.pack(side=TOP, fill=BOTH, expand=1)
        Label(search_pane2, text='Enter Consumer number', anchor='w').pack(side=LEFT)
        Entry(search_pane2, textvariable=self.consumer).pack(side=LEFT)
        self.month.set('January')
        OptionMenu(search_pane2, self.month, *months).pack(side=LEFT)
        OptionMenu(search_pane2, self.year, *years).pack(side=LEFT)
        self.year.set(2019)
        Button(search_pane2, text='Search', command=self.search_db).pack(side=LEFT)

        # results = Frame(self.display, height=220)
        # results.pack()

    def clear_display(self):
        # self.display.pack_propagate(0)
        wid = self.display.winfo_children()
        for w in wid:
            w.destroy()

    def show_db_table(self):
        self.clear_display()
        results = excel.downloadvalues(self.tablename.get())
        hf = Frame(self.display)
        hf.pack(side=TOP, fill=BOTH, expand=1)
        # hf.pack_propagate(0)
        for name in ['ID', 'Consumer', 'Slot', 'Import units', 'Export Units', 'Difference']:
            Label(hf, text=name, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        if results:
            for row in range(len(results)):
                rf = Frame(self.display)
                rf.pack(side=TOP, fill=BOTH, expand=1)
                # rf.pack_propagate(0)
                for val in results[row]:
                    Label(rf, text=val, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        else:
            self.status = Pmw.MessageDialog(self.master, title='No record found', defaultbutton=0, buttons=('OK',), message_text='Not ', command=lambda: print('close message dialog'))

    def search_db(self):

        results = excel.get_consumer_readings(self.consumer.get())
        hf = Frame(self.display)
        hf.pack(side=TOP, fill=BOTH, expand=1)
        # hf.pack_propagate(0)
        for name in ['Slot', 'Import units', 'Export Units', 'Difference']:
            Label(hf, text=name, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        if not results == 'Not available':
            for row in range(len(results)):
                rf = Frame(self.display)
                rf.pack(side=TOP, fill=BOTH, expand=1)
                # rf.pack_propagate(0)
                for val in results[row]:
                    Label(rf, text=val, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        else:
            self.status = Pmw.MessageDialog(self.master, title='No record found', defaultbutton=0, buttons=('OK',), message_text='Not available ', command=lambda btn: print('close message dialog'))
