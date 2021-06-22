from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from datetime import datetime, timedelta

import requests
import re
import pymorphy2
import locale

locale.setlocale(locale.LC_ALL, '')


class RequestTime():
    def __init__(self):
        self.url_time_date = 'https://time100.ru/'
        self.date_time = None

    def get_network_time(self):
        try:
            USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
            headers = {"User-Agent": USERAGENT}
            resp = requests.get('https://time100.ru/', headers=headers)
            http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
            html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
            encoding = html_encoding or http_encoding
            soup = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)

            time = soup.find('h3', {'class': 'display-time monospace'})
            date = soup.find('h3', {'class': 'display-date monospace'})

            # children = data.findChildren()
            time = time.find('span', {'class': 'time'}).text
            date = date.find('span', {'class': 'time'}).text

            date = re.findall(r'[:]\s+(.*)\s+год', date)[0]

            # month_or = re.findall(r'\w+', date)[1]
            #
            # morph = pymorphy2.MorphAnalyzer()
            # month_cus = morph.parse(month_or)[0]
            # month_cus = month_cus.inflect({'nomn'}).word
            # date = re.sub(month_or, month_cus, date)
            #
            # date_time_str = f"{date} {time}"
            # self.date_time = datetime.strptime(date_time_str, '%d %B %Y %H:%M')

            return True
        except Exception as error:
            print(f"$get_network_time {error}")
            return False

    def check_time(self):
        if self.get_network_time():
            expiration_date = datetime.strptime('26 Июнь 2021 23:00', '%d %B %Y %H:%M')
            # print(self.date_time)
            # print(expiration_date)

            if datetime.now() < expiration_date:
                print(f"$До окончания пробного периода: {expiration_date - datetime.now()}")
                return True
            else:
                print(f"$Пробный период закончился!")
                return False
        else:
            print(f"$Нету доступа в ИНТЕРНЕТ!")
