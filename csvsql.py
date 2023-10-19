
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import datetime

connection = None

try:
    connection = mysql.connector.connect(
        user='root',
        password='InitIL-Lg001',
        host='localhost',
        database='ex_history'
    )
    cur = connection.cursor()
    d1 = datetime.datetime(2023,1,1)
    d2 = datetime.datetime(2023,10,17)

    diff = d2-d1

    for i in range(diff.days):
        date = d1 + datetime.timedelta(i)
        try:
            df = pd.read_csv(f'{date.year}-{date.month}-{date.day}.csv')
            
        except:
            continue
        df = df.iloc[1:]
        records = [tuple(x) for x in df.values] 
        
        table_name = f'ex_{date.year}_{date.month}_{date.day}_table'
        create_table_query = f"""
        CREATE TABLE {table_name} (
            currency VARCHAR(20),
            currency_name VARCHAR(20),
            currency_code VARCHAR(4),
            tts VARCHAR(10),
            ttb VARCHAR(10),
            ttm VARCHAR(10)
        )
        """
        cur.execute(create_table_query)
        for j in records:
            cur.execute(f'insert into {table_name} values {j};')
        # insert_query = f"INSERT INTO {table_name} (currency, currency_name, currency_code, tts, ttb, ttm) VALUES (%s, %s, %s, %s, %s, %s)"
        # cur.executemany(insert_query, records)
    connection.commit()
        
    
    print("Connected!")

except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User name or password is invalid.")
    elif e.errno == errorcode.ER_ACCOUNT_HAS_BEEN_LOCKED:
        print("This account is locked.")
    else:
        print(e)

except Exception as e:
    print(f"Error Occurred: {e}")

finally:
    if connection is not None and connection.is_connected():
        # 結果を読み取った後に接続を閉じる
        connection.close()

