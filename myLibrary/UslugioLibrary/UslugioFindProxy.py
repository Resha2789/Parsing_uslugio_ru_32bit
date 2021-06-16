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

        # Запус WebDriverChrome
        m.uslugio_proxy = None
        if not self.star_driver(url=self.url_proxy):
            return

        # Устанавливаем на вебсайт скрипты
        if not self.set_library():
            return

        # Прокси сервера
        m.uslugio_proxy = self.execute_js(tr=2, sl=3, rt=True, t=2, data=f"get_proxy()")
        # Посылаем сигнал на главное окно в прокси
        m.Commun.uslugio_proxy_update.emit(m.uslugio_proxy)
        m.uslugio_found_proxy = True
