from myLibrary.UslugioLibrary.UslugioParsingLib import ParsingUslugio
from PyQt5.QtCore import QThread
from myLibrary import DriverChrome, MainWindow, Slug
import threading


class UslugioThreading(QThread, ParsingUslugio, Slug.Slugify):
    def __init__(self, mainWindow=None, *args, **kwargs):
        self.url = ''
        self.mainWindow = mainWindow
        self.key_word = ''
        super(UslugioThreading, self).__init__(mainWindow=mainWindow, uslugioThreading=self, *args, **kwargs)


    def run(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        threading.Thread(target=self.tim_out_thread).start()

        for i in m.inp_key_words:
            if self.stop_parsing or not m.parsing_uslugio:
                break

            self.key_word = i
            self.url = f"https://uslugio.com/{self.slugify(m.inp_city)}?search={i}"

            # Запус WebDriverChrome
            if not self.star_driver(url=self.url, proxy=False):
                return

            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                return

            # Запускаем цикл парсинга uslugio
            self.start_parsing_uslugio()
