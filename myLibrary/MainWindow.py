import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import QObject
from myLibrary.My_pyqt5 import Uslugio_avito_parsing
from myLibrary.InitialData import InitialData
from myLibrary.UslugioLibrary.UslugioParsing import UslugioThreading
from myLibrary.UslugioLibrary.UslugioFindProxy import UslugioFindProxyThreading
from myLibrary import Loger, Slug
from selenium import webdriver
from get_gecko_driver import GetGeckoDriver

import socket
import time, datetime


class Communicate(QObject):
    uslugio_change = QtCore.pyqtSignal(object)
    avito_change = QtCore.pyqtSignal(object)
    uslugio_yandex_change = QtCore.pyqtSignal(object)
    uslugio_progressBar = QtCore.pyqtSignal(object)
    uslugio_proxy_update = QtCore.pyqtSignal(object)
    uslugio_restart_thread = QtCore.pyqtSignal(object)


class MainWindow(QtWidgets.QMainWindow, Uslugio_avito_parsing.Ui_MainWindow, Loger.OutLogger, Loger.OutputLogger, InitialData, Slug.Slugify):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_md()
        self.uslugio_threading = None
        self.uslugio_find_proxy_threading = None
        self.log = False

        # Конектим пользовательский сигнал на MainWindow
        self.Commun = Communicate()

        self.set_value()
        self.set_connect()

        get_driver = GetGeckoDriver()
        get_driver.install()

    def set_value(self):
        # Город
        self.lineEdit_uslugio_city.setText(self.inp_city)
        # Ключевые слова
        self.lineEdit_uslugio_key_words.setText(self.key_words_str)
        # Прокси сервера
        self.textEdit_uslugio_proxy.setText(self.proxy_str)
        # Показывать браузер
        if self.inp_show_browser:
            self.checkBox_uslugio_show_brawser.setChecked(True)

    def set_connect(self):
        # Поиск прокси
        self.pushButton_uslugio_find_proxy.clicked.connect(self.start_uslugio_find_proxy)
        # СТАРТ парсинга
        self.pushButton_uslugio_start.clicked.connect(self.start_uslugio_thread)
        # СТОП парсинг
        self.pushButton_uslugio_stop.clicked.connect(self.uslugio_stop_threading)
        # Обновляем прогрес бар
        self.Commun.uslugio_progressBar.connect(self.uslugio_progressBar)
        # Обновляем прокси сервера
        self.Commun.uslugio_proxy_update.connect(self.uslugio_proxy_update)
        # Перезагрузка потока UslugioThreading
        self.Commun.uslugio_restart_thread.connect(self.uslugio_restart_threading)

        # Вывод сообщений в консоль
        self.OUTPUT_LOGGER_STDOUT.emit_write.connect(self.append_log)
        self.OUTPUT_LOGGER_STDERR.emit_write.connect(self.append_log)

        # Записываем город
        self.lineEdit_uslugio_city.textChanged.connect(self.set_city)

        # Записываем ключевые слова
        self.lineEdit_uslugio_key_words.textChanged.connect(self.set_key_words)

        # Записываем прокси сервера
        self.textEdit_uslugio_proxy.textChanged.connect(self.set_proxy)

        # Записываем отображение браузера
        self.checkBox_uslugio_show_brawser.clicked.connect(self.set_show_browser)

    def start_uslugio_find_proxy(self):
        # Запускаем дополнительный поток Uslugio.com
        if self.uslugio_find_proxy_threading is None:
            self.uslugio_find_proxy_threading = UslugioFindProxyThreading(mainWindow=self,
                                                                          url='https://hidemy.name/ru/proxy-list/?type=s#list',
                                                                          browser=True,
                                                                          js='myLibrary/JsLibrary/ProxyJsLibrary.js')

        self.log = True
        self.uslugio_find_proxy_threading.start()

    def start_uslugio_thread(self):
        self.parsing_uslugio = True
        self.start_uslugio_find_proxy()

        # Запускаем дополнительный поток Uslugio.com
        if self.uslugio_threading is None:
            self.uslugio_threading = UslugioThreading(mainWindow=self,
                                                      proxy=self.inp_proxy,
                                                      browser=True,
                                                      js='myLibrary/JsLibrary/UslugioJsLibrary.js')

        self.log = True
        self.uslugio_threading.start()

    def uslugio_restart_threading(self, data):
        if self.uslugio_threading is not None:
            if self.uslugio_threading.driver is not None:
                self.uslugio_threading.driver.quit()
                self.uslugio_threading.driver = None
            self.uslugio_threading.close()
            self.uslugio_threading = None
        if self.uslugio_find_proxy_threading is not None:
            if self.uslugio_find_proxy_threading.driver is not None:
                self.uslugio_find_proxy_threading.driver.quit()
                self.uslugio_find_proxy_threading.driver = None
            self.uslugio_find_proxy_threading.close()
            self.uslugio_find_proxy_threading = None
        self.start_uslugio_thread()

    def uslugio_stop_threading(self, data):
        # self.uslugio_threading.driver.refresh()

        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
        driver = webdriver.Firefox(profile)
        driver.get("https://uslugio.com/Ufa?search=%D0%9B%D0%92%D0%A1")
        self.seting_proxy(driver, ssl_addr="51.222.21.93", ssl_port=32768)

        driver.execute_script("console.log('hie')")
        print(driver.title)
        # driver.quit()

        # print(f"uslugio_stop_threading {data}")
        # self.parsing_uslugio = False
        # if self.uslugio_threading is not None:
        #     if self.uslugio_threading.driver is not None:
        #         self.uslugio_threading.driver.quit()
        #         self.uslugio_threading.driver = None
        #         # self.uslugio_threading.driver.driver.get('')
        #         # self.uslugio_threading.driver.quit()
        #     # self.uslugio_threading = None
        #
        # if self.uslugio_find_proxy_threading is not None:
        #     if self.uslugio_find_proxy_threading.driver is not None:
        #         self.uslugio_find_proxy_threading.driver.set_page_load_timeout(0)
        #         self.uslugio_find_proxy_threading.driver.quit()
        #         self.uslugio_find_proxy_threading.driver = None
        #     # self.uslugio_find_proxy_threading = None
        print("Программа завершена")

    # def stop_uslugio_parsing(self):
    #     if self.uslugio_threading is not None:
    #         self.uslugio_threading.stop_parsing = True

    def seting_proxy(self, driver, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):

        driver.execute("SET_CONTEXT", {"context": "chrome"})

        try:
            driver.execute_script("""
              Services.prefs.setIntPref('network.proxy.type', 1);
              Services.prefs.setCharPref("network.proxy.http", arguments[0]);
              Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
              Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
              Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
              Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
              Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
              """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)

        finally:
            driver.execute("SET_CONTEXT", {"context": "content"})

    def append_log(self, text, severity):
        if len(text) > 3:
            if severity == self.Severity.ERROR:
                self.plainTextEdit_uslugio_console.appendPlainText(text)
                self.update_json()
            else:
                self.plainTextEdit_uslugio_console.appendPlainText(text)

    def closeEvent(self, event):
        self.update_json()
        self.parsing_uslugio = False
        if self.uslugio_threading is not None:
            if self.uslugio_threading.driver is not None:
                self.uslugio_threading.driver.quit()
                self.uslugio_threading.driver = None
            self.uslugio_threading = None

        if self.uslugio_find_proxy_threading is not None:
            if self.uslugio_find_proxy_threading.driver is not None:
                self.uslugio_find_proxy_threading.driver.quit()
                self.uslugio_find_proxy_threading.driver = None
            self.uslugio_find_proxy_threading = None

    def set_city(self, val):
        self.inp_city = self.slugify(val)

    def set_key_words(self, val):
        data = re.split(r'[,.]+\s*', val)
        self.inp_key_words = []
        for i in data:
            if len(i) > 1:
                self.inp_key_words.append(i)
        print(self.inp_key_words)

    def set_proxy(self):
        data = re.split(r'[,]+\s*|\n', self.textEdit_uslugio_proxy.toPlainText())
        self.inp_proxy = []
        self.uslugio_verified_proxies = []
        for i in data:
            if len(i) > 1:
                self.inp_proxy.append(i)
                self.uslugio_verified_proxies.append(i)
        print(self.inp_proxy)

    def set_show_browser(self):
        if self.checkBox_uslugio_show_brawser.isChecked():
            self.inp_show_browser = True
        else:
            self.inp_show_browser = False
        # print(self.inp_key_words)
        # print(self.inp_proxy)

    def uslugio_progressBar(self, data):
        percent = (100 / (data['items'] / (data['i'] + 1)))
        self.progressBar_uslugio.setValue(int(percent))

    def uslugio_proxy_update(self, data):
        self.inp_proxy = data
        self.proxy_str = ''
        for i in data:
            self.proxy_str += f"{i}\n"
        self.textEdit_uslugio_proxy.setText(self.proxy_str)
