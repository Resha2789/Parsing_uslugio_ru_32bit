from PyQt5.QtCore import QThread
from myLibrary import DriverChrome


class UslugioFindProxyThreading(QThread, DriverChrome.Execute):
    def __init__(self, parent=None, proxy=None, browser=False, url='', js=''):
        super(UslugioFindProxyThreading, self).__init__(url=url, browser=browser, js=js)
        self.mainWindow = parent
        self.proxy = []

    def run(self):
        # Запус WebDriverChrome
        if not self.star_driver():
            return

        # Устанавливаем на вебсайт скрипты
        if not self.set_library():
            return

        # Прокси сервера
        self.proxy = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy()")
        # Посылаем сигнал на главное окно в прокси
        self.mainWindow.Commun.uslugio_proxy_update.emit(self.proxy)



