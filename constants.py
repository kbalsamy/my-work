import os

global url
global month_dict
global months
global years
global headers_list
global slot_list

url = os.environ.get("login_url")
pword = os.environ.get("p_word")


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = [2018, 2019]

month_dict = {'January': '#mat-option-0 > .mat-option-text', 'February': '#mat-option-1 > .mat-option-text',
              'March': '#mat-option-2 > .mat-option-text', 'April': '#mat-option-3 > .mat-option-text',
              'May': '#mat-option-4 > .mat-option-text', 'June': '#mat-option-5 > .mat-option-text',
              'July': '#mat-option-6 > .mat-option-text', 'August': '#mat-option-7 > .mat-option-text',
              'September': '#mat-option-8 > .mat-option-text', 'October': '#mat-option-9 > .mat-option-text',
              'November': '#mat-option-10 > .mat-option-text', 'December': '#mat-option-11 > .mat-option-text'}


headers_list = ['Consumer Number', 'Import units', 'Export Units', 'Difference']
slot_list = ['C1', "C2", "C3", "C4", "C5"]
