import datetime
import time
import mysql.connector
from mysql.connector import errorcode

import pytz


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



class Scraper:
    def __init__(self) -> None:
        # 1990年以降の為替相場URL:定数
        self.HISTORY_URL = 'http://www.murc-kawasesouba.jp/fx/past_3month.php'
        
        # 外国為替相場一覧表（リアルタイムレート)URL:定数
        self.REALTIME_URL = 'https://www.bk.mufg.jp/ippan/rate/real.html'

        # 今月を含めた5カ月のチャート画像があるURL:定数
        self.CHARTIMG_URL = 'http://www.murc-kawasesouba.jp/fx/index.php' 
        
        # スプレッド
        self.spread = 0
        
        # Chromeをインストール
        driver_path = ChromeDriverManager().install()

        #ブラウザを開く描写をしない
        options = Options()
        # options.add_argument('--headless')  
        options.add_argument('--disable-web-security')

        # ブラウザをChromeに設定
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path),options=options)

    

    def csvdb_update(self):
        # 過去の為替相場検索ページにアクセス
        self.driver.get(self.HISTORY_URL)
        # 西暦
        year = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="yy"]'))

        # 月
        month = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="mm"]'))

        # 日
        day = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="dd"]'))

        decide_btn = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="sbmt"]'))

        year_select = Select(year)

        manth_select = Select(month)

        day_select = Select(day)

        try:
            connection = mysql.connector.connect(
            user='root',
            password='InitIL-Lg001',
            host='localhost',
            database = 'usd_db'
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

        cursor.execute('select max(usd_id) from usd;')
        date_obj = cursor.fetchall()
        date_obj = date_obj[0][0]
        # date_obj = datetime.strptime(max_date, '%Y-%m-%d')
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        d1 = datetime.datetime(date_obj.year,date_obj.month,date_obj.day)+datetime.timedelta(1)
        d2 = datetime.datetime(now.year,now.month,now.day)+datetime.timedelta(1)
        diff = d2-d1
        if diff.days == 0:
            return None
            
        tts_list = []
        ttb_list = []
        date_list = []

        for i in range(diff.days):
            date = d1 + datetime.timedelta(i)
            try:
                year_select.select_by_value(str(date.year))
                manth_select.select_by_value(str(date.month))
                day_select.select_by_value(str(date.day))
                time.sleep(1)
                #　通貨コンボボックスのselect要素選択
                currency = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="cc"]'))
                currency_select = Select(currency)
                currency_select.select_by_visible_text('米ドル')
            except Exception as e:
                print(e)
                continue
            # 検索ボタンをクリック
            decide_btn.click()
            time.sleep(3)
            
            # ウィンドウリスト
            window_list = self.driver.window_handles
            # 検索した通貨のウィンドウに遷移した後に、ドライバーを遷移したウィンドウに切り替える
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(2)
            tts = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[2]/td[4]'))
            ttb = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[2]/td[5]'))
            
            tts_list.append(float(tts.text))
            ttb_list.append(float(ttb.text))
            date_list.append(date.date())
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        
        return {'date':date_list,'tts':tts_list,'ttb':ttb_list}
    
    def post(self,date,tts,ttb):
        try:
            connection = mysql.connector.connect(
            user='root',
            password='InitIL-Lg001',
            host='localhost',
            database = 'usd_db'
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
        
        for i in range(len(date)):
            insert_query = "INSERT INTO usd (usd_id, tts, ttb) VALUES (%s, %s, %s)"
            values = (date[i], tts[i], ttb[i])
            try:
                cursor.execute(insert_query, values)
            except Exception as e:
                print(f'エラーが発生：{e}')
                continue

        # for i in range(len(date)):
        #     try:
        #         cursor.execute(f'insert into usd values ({date[i]},{tts[i]},{ttb[i]})')
        #     except Exception as e:
        #         print(f'エラーが発生：{e}')
        #         continue
        connection.commit()
sc = Scraper()
di = sc.csvdb_update()
sc.post(di['date'],di['tts'],di['ttb'])

