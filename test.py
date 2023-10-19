import mysql.connector
from mysql.connector import errorcode
# import pandas as pd
import datetime
import pytz

try:
    connection = mysql.connector.connect(
    user='root',
    password='InitIL-Lg001',
    host='localhost',
    database = 'ex_history'
)
    cursor = connection.cursor()

except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User name or password is invalid.")
    elif e.errno == errorcode.ER_ACCOUNT_HAS_BEEN_LOCKED:
        print("This account is locked.")
    else:
        print(e)
except Exception as e:
    print(f"Error Occurred: {e}")

cursor.execute('show tables;')
resu = cursor.fetchall()
print(resu[len(resu)-1])
# date_obj = cursor.fetchall()
# date_obj = date_obj[0][0]
# now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

# d1 = datetime.datetime(date_obj.year,date_obj.month,date_obj.day)
# d2 = datetime.datetime(now.year,now.month,now.day)+datetime.timedelta(1)
# diff = d2-d1
# print(date_obj)
# print(diff)