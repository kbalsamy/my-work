from xlsxwriter import Workbook
import sqlite3
from constants import *


def get_table_name(con):

    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = cursor.fetchall()
    tlist = []
    for i in table_list:
        tlist.append(i[0])
    return tlist


def write_excel(results, worksheet):
    r = 0
    c = 0
    for val in results:
        for i in val:
            worksheet.write(r, c, i)
            c += 1
        r += 1
        c = 0


def get_consumer_from_db(cursor, tablename, consumer):
    args = "SELECT * FROM '{}' WHERE consumer = '{}' ;".format(tablename, consumer)
    cursor.execute(args)
    results = cursor.fetchall()
    return results


def get_charges_from_db(cursor, tablename, consumer):
    args = "SELECT code, description, charges FROM '{}' WHERE consumer = '{}' ;".format(tablename, consumer)
    cursor.execute(args)
    results = cursor.fetchall()
    return results


def get_values_from_db(cursor, tablename):
    args = "SELECT * FROM {}".format(tablename)
    cursor.execute(args)
    results = cursor.fetchall()
    return results


def xldownloader(filename, tablename):
    workbook = Workbook(filename)
    con = db_connect()
    cursor = con.cursor()
    readings = get_values_from_db(cursor, tablename)
    worksheet = workbook.add_worksheet('sheet1')
    write_excel(readings, worksheet)
    workbook.close()
    return 'Finished'


# xldownloader('sample.xlsx', 'chargesja2019')
