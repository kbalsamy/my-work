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
        self.top_frame = Frame(self.master, bg='pink', height=100, width=1050)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=1)
        # Middle frame is built with canvas and  then inserted
        # frame within it
        self.canvas = Canvas(self.master, bg='white')
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        scrollbar = Scrollbar(self.canvas, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_configure)

        self.display_frame = Frame(self.canvas, height=450, width=1050, bg='white')
        self.display_frame.pack(side=TOP, fill=BOTH, expand=1)
        # self.display_frame.pack_propagate(0)
        # bottom frame buit with Frame
        self.Botframe = Frame(self.master, bg='yellow', height=100, width=1050)
        self.Botframe.pack(side=TOP, fill=BOTH, expand=1)
        # self.Botframe.pack_propagate(0)
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
        dbframe.databaseFrame(self.top_frame, self.display_frame)

    def build_menu(self):
        # menubar created here
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.menubar.add_command(label='Single Download', command=lambda: print('single Download'))
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

    def on_configure(self, event):
        # update canvas region
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))



# Application instatiation
if __name__ == '__main__':
    root = Tk()
    app = Application(root, 'AMR EXTRACTOR', 1050, 650)
    app.mainloop()
