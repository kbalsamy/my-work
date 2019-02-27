from tkinter import *
from constants import *
import file_creator as excel
import Pmw


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
        search_pane = Frame(self.master, bd=3, relief=GROOVE)
        search_pane.pack(side=TOP, fill=BOTH, expand=1)
        Label(search_pane, text='Search Database here', anchor='w').pack(side=TOP, fill=X, expand=1)
        Label(search_pane, text='Select available Database here', anchor='w').pack(side=LEFT)
        OptionMenu(search_pane, self.tablename, *self.av_db).pack(side=LEFT, anchor='w')
        # unpack the av_db
        if self.av_db[0] == 'Not available':
            btn = Button(search_pane, text='Display', state=DISABLED, command=self.show_db_table)
            btn.pack(side=LEFT)
        else:
            btn = Button(search_pane, text='Display', state=DISABLED, command=self.show_db_table)
            btn.pack(side=LEFT)

        search_pane2 = Frame(self.master, bd=5, relief=GROOVE)
        search_pane2.pack(side=TOP, fill=BOTH, expand=1)
        Label(search_pane2, text='Enter Consumer number', anchor='w').pack(side=LEFT)
        Entry(search_pane2, textvariable=self.consumer).pack(side=LEFT)
        OptionMenu(search_pane2, self.month, *months).pack(side=LEFT)
        OptionMenu(search_pane2, self.year, *years).pack(side=LEFT)
        Button(search_pane2, text='Search', command=lambda: print('seach button clicked')).pack(side=LEFT)

        # results = Frame(self.display, height=220)
        # results.pack()

    def show_db_table(self):
        scrollbar = Scrollbar(self.display)
        scrollbar.pack(side=RIGHT, fill=Y)
        results = excel.downloadvalues(self.tablename.get())
        hf = Frame(self.display)
        hf.pack(side=TOP, fill=BOTH, expand=1)
        for name in ['ID', 'Consumer', 'Slot', 'Import units', 'Export Units', 'Difference']:
            Label(hf, text=name, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        if results:
            for row in range(len(results)):
                rf = Frame(self.display)
                rf.pack(side=TOP, fill=BOTH, expand=1)
                for val in results[row]:
                    Label(rf, text=val, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        else:
            self.status = Pmw.MessageDialog(self.master, title='No record found', defaultbutton=0, buttons=('OK',), message_text='Not ', command=lambda: print('close message dialog'))
