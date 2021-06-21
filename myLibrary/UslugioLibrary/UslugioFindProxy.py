from PyQt5.QtCore import QThread
from myLibrary import DriverChrome
from myLibrary import MainWindow
from datetime import datetime, timedelta
import time


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

        self.find_and_check_proxy()
        self.stop_threading()

        self.working = False


    def stop_threading(self):

        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None

            # self.uslugio_find_proxy_threading = None

        except Exception as error:
            print("ERROR stop_threading:", error)


    def find_and_check_proxy(self):
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

            # Прокси сервера
            m.uslugio_proxy_finded = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy_from_advanced_name()")
            if type(m.uslugio_proxy_finded) == bool:
                self.page = 1
                self.url_proxy = f"https://advanced.name/ru/freeproxy?type=https&page={self.page}"
                return self.find_and_check_proxy()

            for i in m.uslugio_proxy_finded:
                if not m.parsing_uslugio:
                    return

                if self.time_out_proxy is None or datetime.now() > self.time_out_proxy:
                    self.time_out_proxy = datetime.now() + timedelta(minutes=40)
                    m.uslugio_verified_proxies, m.uslugio_used_proxies = [], []

                if not m.parsing_uslugio:
                    break

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
                    return self.find_and_check_proxy()

            # Прокси сервера
            # m.uslugio_proxy_finded = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy()")

            # Проверка найденных прокси url='https://hidemy.name/ru/proxy-list/?type=s#list',
            # for i in m.uslugio_proxy_finded:
            #
            #     if self.time_out_proxy is None or datetime.now() > self.time_out_proxy:
            #         self.time_out_proxy = datetime.now() + timedelta(minutes=5)
            #         m.uslugio_verified_proxies, m.uslugio_used_proxies = [], []
            #
            #     if not m.parsing_uslugio:
            #         break
            #     if len(m.uslugio_verified_proxies) < 10:
            #         if self.proxy_check('https://uslugio.com/', i):
            #             if not i in m.uslugio_verified_proxies and not i in m.uslugio_used_proxies:
            #                 m.uslugio_verified_proxies.append(i)
            #                 # Посылаем сигнал на главное окно в прокси
            #                 m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
            #                 print(f"Прокси сервер найден")
            #     else:
            #         time.sleep(5)
            #
            #     if m.uslugio_proxy_finded[-1] == i:
            #         # Запускаем поиск proxy занаво
            #         return self.find_and_check_proxy()
            #
            # if m.parsing_uslugio:
            #     return self.find_and_check_proxy()
            # else:
            #     return

        except Exception as detail:
            print("ERROR find_and_check_proxy:", detail)
            print("Перезапускаем find_and_check_proxy")
            if m.parsing_uslugio:
                return self.find_and_check_proxy()
            else:
                return
