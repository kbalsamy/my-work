import tkinter
from tkinter import *
from constants import *
import file_creator as excel
import Pmw
import logging
import time
import Create_table_widget as Table
import GUI_APP


class databaseFrame(Frame):

    def __init__(self, master, display, parent, canvas, menu):
        Frame.__init__(self)

        self.master = master
        self.display = display
        self.parent = parent
        self.canvas = canvas
        self.menu = menu

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
        self.op = OptionMenu(search_pane, self.tablename, *self.av_db)
        self.op.pack(side=LEFT, anchor='w')
        # self.op.configure(state="disabled")
        btn2 = Button(search_pane, text='Clear', command=self.clear_display)
        btn2.pack(side=LEFT)
        self.dlbtn = Button(search_pane, text='Download Excel', state=DISABLED, command=self.file_to_save)
        self.dlbtn.pack(side=LEFT)
        # self.checkbuttonvar = IntVar()

        # database search tool
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
        Button(search_pane2, text='Clear', command=self.clear_display).pack(side=LEFT)

    def check_db_latest(self):

        self.menu.entryconfig('Single Download', state='active')

        self.op['menu'].delete(0, 'end')
        for val in self.av_db:
            self.op['menu'].add_command(label=val, command=lambda val=val: self.tablename.set(val))

        if self.tablename.get() == 'Not available' or self.tablename.get() == 'select':
            self.dlbtn.configure(state=DISABLED)
        else:
            self.dlbtn.configure(state=ACTIVE)

    def clear_display(self):
        wid = self.display.winfo_children()
        for w in wid:
            w.destroy()
        self.btn3.configure(state=ACTIVE)
        self.menu.entryconfig('Single Download', state='active')

    def search_db(self):
        self.clear_display()
        self.btn3.configure(state=DISABLED)
        c = self.consumer.getvalue()
        m = self.month.get()
        y = self.year.get()
        tablename1 = m + str(y)
        tablename2 = 'charges' + m[0:2] + str(y)
        cursor = db_connect().cursor()
        readings = excel.get_consumer_from_db(cursor, tablename1, c)
        charges = excel.get_charges_from_db(cursor, tablename2, c)
        if readings and charges:
            results = results_compact(readings, charges)
            manager = Table.Plotter(self.display)
            manager.plot_values(results)
            timestr = time.asctime()
            logging.info('{} : Data fetched for {}'.format(timestr, self.consumer.getvalue()))

        else:
            self.status = Pmw.MessageDialog(self.master, title='Status', defaultbutton=0, buttons=('OK',), message_text='Data not found for {}'.format(self.consumer.get()), command=self.close_status)
            self.status.activate(geometry='centerscreenfirst')
            timestr = time.asctime()
            logging.info('{} : Data not found for {}'.format(timestr, self.consumer.getvalue()))
            self.btn3.configure(state=ACTIVE)

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
