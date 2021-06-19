import time

from PyQt5.QtCore import QThread
from myLibrary import DriverChrome
from myLibrary import MainWindow


class UslugioFindProxyThreading(QThread, DriverChrome.Execute):
    def __init__(self, mainWindow=None, *args, **kwargs):
        super(UslugioFindProxyThreading, self).__init__(mainWindow=mainWindow, *args, **kwargs)
        self.mainWindow = mainWindow
        m: MainWindow.MainWindow
        m = self.mainWindow
        self.url_proxy = kwargs.get('url')

    def run(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.find_and_check_proxy()

    def find_and_check_proxy(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            # Запус WebDriverChrome
            if not self.star_driver(url=self.url_proxy, proxy=False):
                return
            # time.sleep(20)

            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                return

            # Прокси сервера
            m.uslugio_proxy_finded = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy()")

            # Проверка найденных прокси
            for i in m.uslugio_proxy_finded:
                if not m.parsing_uslugio:
                    break
                if len(m.uslugio_verified_proxies) < 5:
                    if self.proxy_check('https://uslugio.com/', i):
                        if not i in m.uslugio_verified_proxies and not i in m.uslugio_used_proxies:
                            m.uslugio_verified_proxies.append(i)
                            # Посылаем сигнал на главное окно в прокси
                            m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
                else:
                    time.sleep(5)

                if m.uslugio_proxy_finded.index(i) > 10 or m.uslugio_proxy_finded[-1] == i:
                    # Запускаем поиск proxy занаво
                    return self.find_and_check_proxy()

            if m.parsing_uslugio:
                return self.find_and_check_proxy()
            else:
                return

        except Exception as detail:
            print("ERROR find_and_check_proxy:", detail)
            print("Перезапускаем find_and_check_proxy")
            if m.parsing_uslugio:
                return self.find_and_check_proxy()
            else:
                return
