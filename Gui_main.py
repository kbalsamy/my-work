# modulues
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import Pmw
from constants import *
import Create_table_widget as Table
import extractor
import batch_extractor as downloader
import database_frame as dbframe
import file_creator as excel
from queue import Queue
import queue
import threading
import log
import logging
import time


def get_uname(file):
    if file:
        with open(file, 'r') as file:
            return [uname.strip() for uname in file]
    else:
        pass


class Application(Frame):

    def __init__(self, master, title, height, width):
        Frame.__init__(self)
        self.Topframe = Frame(self.master, height=100, width=1050)
        self.Topframe.pack(side=TOP, fill=BOTH, expand=1)
        self.Cdisplay = Canvas(self.master, height=450, width=1050, bd=3, relief=GROOVE, bg='white')
        self.Cdisplay.pack(side=TOP, fill=BOTH, expand=1)
        self.displayframe = Frame(self.Cdisplay)
        self.displayframe.pack(side=TOP, fill=BOTH, expand=1)
        self.Botframe = Frame(self.master, height=100, width=1050)
        self.Botframe.pack(side=TOP, fill=BOTH, expand=1)
        self.master = master
        self.master.resizable(False, False)
        self.title = title
        self.height = height
        self.width = width
        self.master.title(self.title)
        self.master.geometry('%dx%d' % (height, width))
        #  build menu options on Main frame widget
        self.build_menu()
        db = dbframe.databaseFrame(self.Topframe, self.Cdisplay)
        self.progressbar = ttk.Progressbar(self.Botframe, orient='horizontal', mode='determinate')
        self.progressbar.pack(side=BOTTOM, fill=X, expand=1, anchor='s')
        self.log_window = ScrolledText.ScrolledText(self.Botframe, state='disabled')
        self.log_window.pack(side=BOTTOM, fill=BOTH, anchor='s')
        self.log_handler = log.TextHandler(self.log_window)
        logging.basicConfig(filename='AMRapplication.log',
                            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.addHandler(self.log_handler)
        self.queue = Queue()

    def build_menu(self):
        # menubar created here
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.menubar.add_command(label='Single Download', command=self.show_sd_dialog)
        self.menubar.add_command(label='Batch Download', command=self.show_batch_dialog)
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

    def check_sd_results(self):
        #  checking queue objects for results, if results, then dispalyed here
        try:
            results = self.queue.get(0)
            self.progressbar.stop()
            Button(self.displayframe, text='Clear', command=self.clear_displayframe).pack()
            manager = Table.Table_creator(self.displayframe)
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
        # results = extractor.scrape(consumerNo, password, mnth, yr)
        results = [['079204720584'], ['171', '333', '153', '648', '828', '46962', '15246', '5130', '163125',
                                      '57006', '46791.0', '14913.0', '4977.0', '162477.0', '56178.0']]
        queue.put(results)

    def clear_displayframe(self):

        for wid in self.displayframe.winfo_children():
            wid.destroy()
        self.menubar.entryconfig('Single Download', state='active')

    def close_errordialog(self, button):
        self.errordialog.deactivate()

    def show_batch_dialog(self):

        self.bd_month = StringVar()
        self.bd_year = IntVar()
        self.bdownload = Pmw.Dialog(self.master, title='Batch Service Download', buttons=('Download', 'Cancel'), defaultbutton='Search', command=self.execute_bdownload)
        Message(self.bdownload.interior(), text='*This Option will work only, \n if password is same for all service', justify=LEFT, width=350).pack(side=TOP, fill=X, expand=1)
        Label(self.bdownload.interior(), text='Upload .txt file here').pack()
        Button(self.bdownload.interior(), text='upload', command=self.upload_file).pack()
        self.bd_month.set('January')
        OptionMenu(self.bdownload.interior(), self.bd_month, *months).pack()
        self.bd_year.set(2019)
        OptionMenu(self.bdownload.interior(), self.bd_year, *years).pack()
        self.bdownload.activate(geometry='centerscreenfirst')

    def execute_bdownload(self, button):
        if button == 'Download':
            self.pword_dialog = Pmw.PromptDialog(self.master, title='Password', label_text='Password:', entryfield_labelpos='n', entry_show='*', defaultbutton=0, buttons=('OK', 'Cancel'))
            self.pword_dialog.activate(geometry='centerscreenfirst')
            self.bdownload.deactivate()
            self.progressbar.start()
            # place thread here
            threading.Thread(target=self.get_batch_results, args=(self.queue,)).start()
            self.master.after(100, self.show_batch_results)
        else:
            self.bdownload.deactivate()

    def show_batch_results(self):
        self.menubar.entryconfig('Batch Download', state='disabled')
        try:
            results = self.queue.get(0)
            self.progressbar.stop()
            self.messbox = Pmw.MessageDialog(self.master, title='Batch download status', message_text=' Download completed', buttons=('Display', 'OK'), command=self.db_spread_display)
            self.messbox.activate(geometry='centerscreenfirst')
            timestr = time.asctime()
            logging.info('{} Batch download is completed'.format(timestr))
            b = Button(self.displayframe, text='Download', command=self.file_to_save)
            b.pack()

        except queue.Empty:
            self.master.after(100, self.show_batch_results)

    def upload_file(self):

        file = filedialog.askopenfilename()
        service_list = get_uname(file)
        self.service_list = service_list

    def get_batch_results(self, queue):
        results = downloader.main(self.service_list, self.pword_dialog.get(), self.bd_month.get(), self.bd_year.get())
        queue.put(results)

    def db_spread_display(self, button):
        self.menubar.entryconfig('Batch Download', state='active')
        if button == 'Display':
            print('show results')
        else:
            self.messbox.deactivate()

    def file_to_save(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Excel workbook", "*.xlsx"), ("all files", "*.*")))
        # print(filename)
        if filename is None:
            return
        tablename = self.bd_month.get() + str(self.bd_year.get())
        d = excel.xldownloader("{}.xlsx".format(filename), tablename)
        dialog = Pmw.MessageDialog(self.master, title='Download status', defaultbutton=0, buttons=('OK',),
                                   message_text='Excel file download completed')



# Application instatiation
if __name__ == '__main__':
    root = Tk()
    app = Application(root, 'AMR EXTRACTOR', 1050, 650)
    app.mainloop()
