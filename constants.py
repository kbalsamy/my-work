import os
import sqlite3
import itertools

global url
global month_dict
global months
global years
global headers_list
global slot_list
global sections
global banking
global chargesCodeList
global month_selector

url = "http://htoa.tnebnet.org/oa/login/login"


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = [2018, 2019]

month_dict = {'January': '#mat-option-0 > .mat-option-text',
              'February': '#mat-option-1 > .mat-option-text',
              'March': '#mat-option-2 > .mat-option-text', 'April': '#mat-option-3 > .mat-option-text',
              'May': '#mat-option-4 > .mat-option-text', 'June': '#mat-option-5 > .mat-option-text',
              'July': '#mat-option-6 > .mat-option-text', 'August': '#mat-option-7 > .mat-option-text',
              'September': '#mat-option-8 > .mat-option-text', 'October': '#mat-option-9 > .mat-option-text',
              'November': '#mat-option-10 > .mat-option-text', 'December': '#mat-option-11 > .mat-option-text'}


month_selector = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}


sections = {'reading': ".mat-list-item:nth-child(2) span:nth-child(1)",
            'statement': "mat-list-item:nth-child(3) span:nth-child(1)"}

banking = ['mat-input-22', 'mat-input-23', 'mat-input-24', 'mat-input-25', 'mat-input-26']


headers_list = ['Consumer Number', 'Import units', 'Export Units', 'Difference']
slot_list = ['C1', "C2", "C3", "C4", "C5"]

sample = ['079204720584', '079204720585']

sample_results = ['079204720584',
                  ['171', '333', '153', '648', '828', '46962', '15246', '5130', '163125', '57006',
                   46791.0, 14913.0, 4977.0, 162477.0, 56178.0, '6307', '9747', '6105', '66715', '13983'],
                  ['C002', 'O&M Charges', '49384', 'C003', 'Transmission Charges', '115798',
                   'C004', 'System Operation Charges', '1287', 'C005', 'RKvah Penalty', '29651',
                   'C006', 'Negative Energy Charges', '', 'C007', 'Scheduling Charges', '4880',
                   'C001', 'Meter Reading Charges', '300']]


def make_dict_charges(values):

  chargesCodeList = {}
  e1 = values[2]
  x = 0
  y = 1
  while y <= 21:
    chargesCodeList[e1[x]] = e1[y]
    x += 3
    y = x + 1
  return chargesCodeList


def results_compact(readings, charges):

  results = []
  for row in readings:
    s1 = row[0]
    results.append(s1)
    s2 = row[1:]
    results.append(s2)
    results.append(charges)
  return results


def db_connect():

  connect = sqlite3.connect('ReadingsV1onAPP.db')
  return connect


m = ['079204720584', ['234', '153', '54', '684', '486', '17973', '12645', '3573', '63648', '28233', 17739.0, 12492.0, 3519.0, 62964.0, 27747.0, '6307', '4490', '7960', '75115', '13983.86'], [['C002', 'O&M Charges', '22668'], ['C003', 'Transmission Charges', '53153'], ['C004', 'System Operation Charges', '591'], ['C005', 'RKvah Penalty', '1242'], ['C006', 'Negative Energy Charges', '0'], ['C007', 'Scheduling Charges', '2240'], ['C001', 'Meter Reading Charges', '300']]]
