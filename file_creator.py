from xlsxwriter import Workbook
import sqlite3


def db_connect():

    con = sqlite3.connect('ReadingsV1onAPP.db')
    return con


def get_table_name(con):

    cursor = db_connect()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = cursor.fetchall()
    t, u = (table_list)
    table_name = t[0]
    return table_name


def get_consumer_list(con, tablename):

    cursor = con.cursor()
    arg = "SELECT consumer Connection FROM {}". format(tablename)
    cursor.execute(arg)
    results = cursor.fetchall()
    # print(results)
    return results


def get_queries_from_db(con, tablename):
    table_name = tablename
    cursor = con.cursor()
    result_container = []

    for i in ['C1', "C2", "C3", "C4", "C5"]:
        args = "SELECT ImportUnits, ExportUnits, DifUnits FROM {} WHERE  Connection = '{}'".format(tablename, i)
        cursor.execute(args)
        result = cursor.fetchall()
        result_container.append(result)
    return result_container


def write_cons_excel(row, column, db_results, worksheet):
    r = row
    c = column
    previous_consumer = None
    for cons in db_results:
        consumer = cons[0]
        if consumer != previous_consumer or consumer == None:
            worksheet.write(r, c, consumer)
            r += 1
            previous_consumer = consumer

        else:
            pass


def write_excel(row, column, db_results, worksheet, workbook):
    r = row
    c = column
    for result in db_results:
        imp, exp, dif = (result)
        worksheet.write(r, c, imp)
        worksheet.write(r, c + 5, exp)
        worksheet.write(r, c + 10, dif)
        r += 1


def writer(con, tablename, workbook, worksheet):
    cons = get_consumer_list(con, tablename)
    results = get_queries_from_db(con, tablename)
    write_cons_excel(0, 0, cons, worksheet)
    c = 1
    for i in results:
        write_excel(0, c, i, worksheet, workbook)
        c += 1


def xldownloader(filename, tablename):
    workbook = Workbook(filename)
    con = sqlite3.connect('ReadingsV1onAPP.db')
    worksheet = workbook.add_worksheet('sheet1')
    writer(con, tablename, workbook, worksheet)
    workbook.close()
    return 'Finished'


def downloadvalues(tablename):

    results = []
    con = sqlite3.connect('ReadingsV1onAPP.db')
    cursor = con.cursor()
    arg = "SELECT * FROM {}".format(tablename)
    cursor.execute(arg)
    results = cursor.fetchall()
    # print(results)
    # for i in results:
    #     print(i)
    return results

print(downloadvalues('January2019'))
print(downloadvalues('chargesja2019'))


def get_table_name():

    options = []
    con = sqlite3.connect('ReadingsV1onAPP.db')
    cursor = con.cursor()
    args = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(args)
    table_list = cursor.fetchall()
    if len(table_list) == 0:
        # print('no values')
        return ('Not available',)
        # need to fix
    else:
        t, _ = (table_list)
        return t


def get_consumer_readings(connectionNumber):
    con = sqlite3.connect('ReadingsV1onAPP.db')
    cursor = con.cursor()
    args = "SELECT connection, ImportUnits, ExportUnits, DifUnits FROM 'January2019' WHERE consumer = '{}'".format(connectionNumber)
    cursor.execute(args)
    results = cursor.fetchall()
    # print(len(results))
    if len(results) == 0:
        return ('Not available',)
    return results


# print(get_consumer_readings('079204720584'))
# downloadvalues('January2019')

# xldownloader('C:/Users/home/Documents/sample.xlsx', 'January2019')
