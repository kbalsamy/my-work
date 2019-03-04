from tkinter import *
from constants import *
import file_creator as excel
import Pmw
import logging
import time


class databaseFrame(Frame):

    def __init__(self, master, display, parent, canvas):
        Frame.__init__(self)
        self.master = master
        self.display = display
        self.parent = parent
        self.canvas = canvas
        self.month = StringVar()
        self.year = IntVar()
        self.tablename = StringVar()
        self.av_db = excel.get_table_name(db_connect())

        # creaing searching pane tool bar
        search_pane = Frame(self.master, bd=2, relief=GROOVE)
        search_pane.pack(side=TOP, fill=BOTH, expand=1)
        self.refresh = Button(search_pane, text='Refresh', command=self.check_db_latest).pack(side=TOP)
        Label(search_pane, text='Search Database here', anchor='w').pack(side=TOP, fill=X, expand=1)
        Label(search_pane, text='Select available Database here', anchor='w').pack(side=LEFT)
        self.tablename.set('select')
        self.op = OptionMenu(search_pane, self.tablename, *self.av_db, command=self.getTablename)
        self.op.pack(side=LEFT, anchor='w')
        btn2 = Button(search_pane, text='Clear', command=lambda: self.clear_display(btn1=True))
        btn2.pack(side=LEFT)
        self.dlbtn = Button(search_pane, text='Download Excel', state=DISABLED, command=self.file_to_save)
        self.dlbtn.pack(side=LEFT)

        search_pane2 = Frame(self.master, bd=5, relief=GROOVE)
        search_pane2.pack(side=TOP, fill=BOTH, expand=1)
        self.consumer = Pmw.EntryField(search_pane2, labelpos=W, label_text='Consumer Number', validate='numeric')
        self.consumer.pack(side=LEFT)
        self.month.set('January')
        OptionMenu(search_pane2, self.month, *months).pack(side=LEFT)
        OptionMenu(search_pane2, self.year, *years).pack(side=LEFT)
        self.year.set(2019)
        self.btn3 = Button(search_pane2, text='Search', command=self.search_db)
        self.btn3.pack(side=LEFT)
        Button(search_pane2, text='Clear', command=lambda: self.clear_display(btn2=True)).pack(side=LEFT)

    def check_db_latest(self):
        self.av_db = excel.get_table_name(db_connect())
        menu = self.op['menu']
        menu.delete(0, 'end')
        for val in self.av_db:
            menu.add_command(label=val, command=lambda: self.tablename.set(val))

        if self.tablename.get() == 'Not available' or self.tablename.get() == 'select':
            self.dlbtn.configure(state=DISABLED)
        else:
            self.dlbtn.configure(state=ACTIVE)

    def getTablename(self, event):
        # function used to check the optionmenu selection and trigger button availabilty
        selected = self.tablename.get()
        if self.tablename.get() == 'Not available' or self.tablename.get() == 'select':
            self.dlbtn.configure(state=DISABLED)
        else:
            self.dlbtn.configure(state=ACTIVE)

    def clear_display(self, btn1=None, btn2=None):
        wid = self.display.winfo_children()
        for w in wid:
            w.destroy()
        self.btn3.configure(state=ACTIVE)

    def show_db_table(self):
        self.btn1.configure(state=DISABLED)
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
                    current = StringVar()
                    current.set(val)
                    Entry(rf, textvariable=current, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
            timestr = time.asctime()
            logging.info('{} : Data fetched for {}'.format(timestr, self.tablename.get()))
        else:
            self.status = Pmw.MessageDialog(self.master, title='No record found', defaultbutton=0, buttons=('OK',), message_text='Not ', command=lambda: print('close message dialog'))
            timestr = time.asctime()
            logging.info('{} : Data not found for {}'.format(timestr, self.tablename.get()))

        self.parent.update()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def search_db(self):
        self.btn3.configure(state=DISABLED)
        results = excel.get_consumer_readings(self.consumer.get())
        hf = Frame(self.display)
        hf.pack(side=TOP, fill=BOTH, expand=1)
        for name in ['Slot', 'Import units', 'Export Units', 'Difference']:
            Label(hf, text=name, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
        if not results[0] == 'Not available':
            for row in range(len(results)):
                rf = Frame(self.display)
                rf.pack(side=TOP, fill=BOTH, expand=1)
                for val in results[row]:
                    Label(rf, text=val, relief=SOLID, bd=1, width=20).pack(side=LEFT, fill=X, expand=1)
            timestr = time.asctime()
            logging.info('{} : Data fetched for {}'.format(timestr, self.consumer.get()))

        else:
            self.status = Pmw.MessageDialog(self.master, title='Status', defaultbutton=0, buttons=('OK',), message_text='Data not found for {}'.format(self.consumer.get()), command=self.close_status)
            self.status.activate(geometry='centerscreenfirst')
            timestr = time.asctime()
            logging.info('{} : Data not found for {}'.format(timestr, self.consumer.get()))

    def close_status(self, button):
        self.status.deactivate()

    def file_to_save(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Excel workbook", "*.xlsx"), ("all files", "*.*")))

        if filename:
            tablename = self.tablename.get()
            d = excel.xldownloader("{}.xlsx".format(filename), tablename)
            if d == 'Finished':
                logging.info('Excel file download Finished')
        else:
            timestr = time.asctime()
            logging.info('{} : Excel file Download Cancelled'.format(timestr))
