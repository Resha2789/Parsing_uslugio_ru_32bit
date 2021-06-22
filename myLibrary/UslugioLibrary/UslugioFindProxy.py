from PyQt5.QtCore import QThread
from myLibrary import DriverChrome
from myLibrary import MainWindow
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import locale
import re
import time

locale.setlocale(locale.LC_ALL, '')


class UslugioFindProxyThreading(QThread, DriverChrome.Execute):
    def __init__(self, mainWindow=None, *args, **kwargs):
        super(UslugioFindProxyThreading, self).__init__(mainWindow=mainWindow, *args, **kwargs)
        self.mainWindow = mainWindow
        m: MainWindow.MainWindow
        m = self.mainWindow
        self.url_proxy = kwargs.get('url')
        self.time_out_proxy = None
        self.working = False
        self.page = 1

    def run(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.working = True

        if m.inp_auto_get_proxy:
            self.auto_input_and_check_proxy()
        else:
            self.manual_input_and_check_proxy()

        self.stop_threading()

        self.working = False

    def stop_threading(self):

        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None

        except Exception as error:
            print("ERROR stop_threading:", error)

    def manual_input_and_check_proxy(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            if not m.parsing_uslugio:
                return

            m.uslugio_proxy_finded = open(m.inp_path_manual_proxy).read().split('\n')

            for i in m.uslugio_proxy_finded:
                if not m.parsing_uslugio:
                    return

                if self.proxy_check('https://uslugio.com/', i):
                    if not i in m.uslugio_verified_proxies and not i in m.uslugio_used_proxies:
                        m.uslugio_verified_proxies.append(i)
                        # Посылаем сигнал на главное окно в прокси
                        m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
                        print(f"Подходящий прокси сервер найден")

            time.sleep(5)
            return self.manual_input_and_check_proxy()

        except Exception as error:
            print(f"ERROR manual_input_and_check_proxy {error}")
            time.sleep(5)

        return False

    def auto_input_and_check_proxy(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            if not m.parsing_uslugio:
                return

            # Запус WebDriverChrome
            if not self.star_driver(url=self.url_proxy, proxy=False):
                return
            time.sleep(10)

            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                return

            if re.search(r'advanced', self.url_proxy):
                # Прокси сервера
                m.uslugio_proxy_finded = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy_from_advanced_name()")

                if type(m.uslugio_proxy_finded) == bool:
                    self.page = 1
                    self.url_proxy = f"https://advanced.name/ru/freeproxy?type=https&page={self.page}"
                    return self.manual_input_and_check_proxy()

                for i in m.uslugio_proxy_finded:
                    if not m.parsing_uslugio:
                        return

                    # if self.time_out_proxy is None or datetime.now() > self.time_out_proxy:
                    #     self.time_out_proxy = datetime.now() + timedelta(minutes=40)
                    #     m.uslugio_verified_proxies, m.uslugio_used_proxies = [], []

                    if self.proxy_check('https://uslugio.com/', i):
                        if not i in m.uslugio_verified_proxies and not i in m.uslugio_used_proxies:
                            m.uslugio_verified_proxies.append(i)
                            # Посылаем сигнал на главное окно в прокси
                            m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
                            print(f"Подходящий прокси сервер найден")

                    if m.uslugio_proxy_finded[-1] == i:
                        self.page += 1
                        self.url_proxy = f"https://advanced.name/ru/freeproxy?type=https&page={self.page}"
                        # Запускаем поиск proxy занаво
                        return self.manual_input_and_check_proxy()

        except Exception as detail:
            print("ERROR find_and_check_proxy:", detail)
            if m.parsing_uslugio:
                return self.manual_input_and_check_proxy()
            else:
                return