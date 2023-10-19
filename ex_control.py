
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import datetime

class ExControl:
    def __init__(self) -> None:
        try:
            self.connection = mysql.connector.connect(
            user='root',
            password='InitIL-Lg001',
            host='localhost',
            
        )
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password is invalid.")
            elif e.errno == errorcode.ER_ACCOUNT_HAS_BEEN_LOCKED:
                print("This account is locked.")
            else:
                print(e)
        except Exception as e:
            print(f"Error Occurred: {e}")

    def ex_history_get(self,year,month,day):
        try:
            cursor = self.cursor
            cursor.execute('use ex_history;')
            cursor.execute(f'SELECT * FROM ex_{year}_{month}_{day}_table;')
            result = cursor.fetchall()
            df = pd.DataFrame(result,columns=['Currency','通貨名','略称 Code','TTS','TTB','TTM'])
        except:
            return 'error'
        return {'csv': df.to_csv().encode('utf_8_sig'),'table_html':df.to_html()}

    def ex_usd_get(self):
        cursor = self.cursor
        cursor.execute('use usd_db')
        cursor.execute(f'SELECT * FROM usd;')
        result = cursor.fetchall()
        df = pd.DataFrame(result,columns=['usd_id','tts','ttb'])
        return df
        # fig = px.line(df,x='date',y=['tts','ttb'],title="USD 4-Moth Chart")
        # st.plotly_chart(fig, use_container_width=True)



