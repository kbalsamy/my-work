import sqlite3

con = sqlite3.connect('ReadingsV1onAPP.db')
cursor = con.cursor()
tablename1 = 'January2019'
tablename2 = 'chargesja2019'
consumerNo = '079204720584'
args1 = "SELECT * FROM {} WHERE consumer = '{}'".format(tablename1, consumerNo)
cursor.execute(args1)
readings = cursor.fetchall()
args2 = "SELECT * FROM {} WHERE consumer = '{}'".format(tablename2, consumerNo)
cursor.execute(args2)
chrgs = cursor.fetchall()

print(readings, '\n')
readings.pop(0)
print(readings, '\n')


# print(chrgs)

f = [readings + chrgs]

print(f)
