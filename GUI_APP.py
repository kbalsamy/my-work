# modulues
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import Pmw
from constants import *
from queue import Queue
import queue
import threading
import log
import logging
import time
import database_frame as dbframe
import extractor
import Create_table_widget as Table


class Application(Frame):

    def __init__(self, master, title, height, width):
        Frame.__init__(self)
        self.master = master
        self.master.resizable(False, False)
        self.title = title
        self.height = height
        self.width = width
        self.master.title(self.title)
        self.master.geometry('%dx%d' % (height, width))
        # Seperating working regions into three
        # Top frame built using Frame widgets
        self.top_frame = Frame(self.master, bg='pink', width=1050)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.top_frame.pack_propagate(0)
        # Middle frame is built with canvas and  then inserted
        # frame within it
        self.canvas = Canvas(self.master, bg='white')
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.pack_propagate(0)
        scrollbar = Scrollbar(self.canvas, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.display_frame = Frame(self.canvas, bg='white')
        self.display_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.create_window((20, 0), window=self.display_frame, anchor='nw', width=1000)
        #         # bottom frame buit with Frame
        self.Botframe = Frame(self.master, bg='yellow', width=1050)
        self.Botframe.pack(side=TOP, fill=BOTH, expand=1)
        self.Botframe.pack_propagate(0)
        # Menu GUI built call
        self.build_menu()
        # Progress bar built
        self.progressbar = ttk.Progressbar(self.Botframe, orient='horizontal', mode='determinate')
        self.progressbar.pack(side=BOTTOM, fill=X, expand=1, anchor='s')
        self.log_window = ScrolledText.ScrolledText(self.Botframe, state='disabled', bg='yellow')
        self.log_window.pack(side=BOTTOM, fill=BOTH, anchor='s')
        self.log_handler = log.TextHandler(self.log_window)
        logging.basicConfig(filename='AMRapplication.log',
                            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.addHandler(self.log_handler)
        self.queue = Queue()
        # database table query widget frame
        dbframe.databaseFrame(self.top_frame, self.display_frame, self.master, self.canvas)

    def build_menu(self):
        # menubar created here
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.menubar.add_command(label='Single Download', command=self.show_sd_dialog)
        self.menubar.add_command(label='Batch Download', command=lambda: print('Batch Download'))
        self.menubar.add_command(label='About', command=self.show_about_dialog)

    def show_about_dialog(self):
        # About dialog frame created here using Pmw
        Pmw.aboutversion('1.0')
        Pmw.aboutcopyright('Copyright Thiran Softwares 2019\nAll rights reserved')
        Pmw.aboutcontact(
            'For information about this application contact:\n' +
            '  My Help Desk\n' +
            '  Phone: +91 9176961009\n' +
            '  email: help@thiransoftwares.com'
        )
        about = Pmw.AboutDialog(self.master, title='About AMR Extractor', buttons=('OK',))
        about.activate(geometry='centerscreenfirst')

    def show_sd_dialog(self):
        # Single download dialog created here
        self.consumer_month = StringVar()
        self.consumer_year = IntVar()
        self.sdd = Pmw.Dialog(self.master, title='Single Service Download', buttons=('Search', 'Cancel'), defaultbutton='Search', command=self.execute_sd)
        self.consumer_entry = Pmw.EntryField(self.sdd.interior(), labelpos='n', label_text='Consumer Number',
                                             validate='numeric')
        self.consumer_entry.pack()
        self.consumer_pass = Pmw.EntryField(self.sdd.interior(), labelpos='n', label_text='Password',
                                            entry_show='*', validate=None)
        self.consumer_pass.pack()

        consumer_month = Pmw.OptionMenu(self.sdd.interior(), labelpos='w', label_text='Choose Month:',
                                        menubutton_textvariable=self.consumer_month, items=months)
        consumer_month.setvalue('January')
        consumer_month.pack()
        consumer_year = Pmw.OptionMenu(self.sdd.interior(), labelpos='w', label_text='Choose Year:',
                                       menubutton_textvariable=self.consumer_year, items=years)
        consumer_year.setvalue(2019)
        consumer_year.pack()
        self.sdd.activate(geometry='centerscreenfirst')

    def execute_sd(self, button):
        self.menubar.entryconfig('Single Download', state='disabled')
        if button == 'Search':
            # validate the entries first before passing to a function
            if len(self.consumer_entry.getvalue()) == 12:
                self.sdd.deactivate()
                self.progressbar.configure(mode='indeterminate')
                thread1 = threading.Thread(target=self.get_sd_results, kwargs={'queue': self.queue})
                thread1.start()
                self.progressbar.start()
                self.master.after(100, self.check_sd_results)

            else:
                self.errordialog = Pmw.MessageDialog(self.master, title='Retry', defaultbutton=0, buttons=('OK',), message_text='Not a valid Consumer number', command=self.close_errordialog)
                self.errordialog.activate()
        else:
            self.sdd.deactivate()
            self.menubar.entryconfig('Single Download', state='active')

    def check_sd_results(self):
        #  checking queue objects for results, if results, then dispalyed here
        try:
            results = self.queue.get(0)
            self.progressbar.stop()
            Button(self.display_frame, text='Clear', command=self.clear_displayframe).pack()
            manager = Table.Table_creator(self.display_frame)
            manager.exim_table('Service Number')
            manager.exim_table('Import Units', single_header=False)
            manager.exim_table('Export Units', single_header=False)
            manager.exim_table('Difference', single_header=False)
            manager.add_row(results)

        except queue.Empty:
            self.master.after(100, self.check_sd_results)

    def get_sd_results(self, queue):
        #  concurrently getting the results via thread and store in the queue objects
        consumerNo = self.consumer_entry.getvalue()
        password = self.consumer_pass.getvalue()
        mnth = self.consumer_month.get()
        yr = self.consumer_year.get()
        results = extractor.scrape(uname=consumerNo, password, mnth, yr)
        # results = [['079204720584'], ['171', '333', '153', '648', '828', '46962', '15246', '5130', '163125',
                                      # '57006', '46791.0', '14913.0', '4977.0', '162477.0', '56178.0']]
        queue.put(results)

    def clear_displayframe(self):

        for wid in self.display_frame.winfo_children():
            wid.destroy()
        self.menubar.entryconfig('Single Download', state='active')

    def close_errordialog(self, button):
        self.errordialog.deactivate()



# Application instatiation
if __name__ == '__main__':
    root = Tk()
    app = Application(root, 'AMR EXTRACTOR', 1050, 650)
    app.mainloop()
