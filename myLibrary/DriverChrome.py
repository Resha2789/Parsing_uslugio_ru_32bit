import re
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from myLibrary import ProxyCheck
from myLibrary import MainWindow
from datetime import datetime, timedelta
import time


# Запуск WebDriverChrome
# url='', proxy=None, browser=False
class StartDriver(ProxyCheck.ProxyCheck):
    def __init__(self, mainWindow=None, url='', proxy=None, browser=False):
        super().__init__()
        self.mainWindow = mainWindow
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.driver_path = 'geckodriver.exe'
        self.driver = None
        self.show_browser = browser
        self.driver_closed = False
        self.set_url = url
        self.total_person = None
        self.time_out = 0
        self.proxy_installed = False

    def star_driver(self, url=None, proxy=True):
        m: MainWindow.MainWindow
        m = self.mainWindow

        if not m.parsing_uslugio:
            return

        self.set_url = url

        if self.driver is not None:
            try:
                print(f"DRIVER QUIT")
                self.driver.quit()
                time.sleep(4)
                self.driver = None
            except Exception as detail:
                self.driver = None
                print("ERROR DRIVER QUIT:", detail)

        print(f"DRIVER START")

        try:
            # Запускаем webDriverFirefox
            profile = self.get_profile()[0]
            options = self.get_profile()[1]
            self.driver = webdriver.Firefox(executable_path=self.driver_path, firefox_profile=profile, options=options)
            self.driver.get(url)

            print("Заргузка страницы успешна прошла.")

        except Exception as detail:
            # self.driver_closed = False
            print(f"ERROR star_driver: {self.set_url}", detail)
            print("Перезапускаем star_driver")
            return self.star_driver(url=self.set_url, proxy=proxy)

        return True

    # Timeout update website 5min
    def tim_out_thread(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        while m.parsing_uslugio:
            try:
                if not m.parsing_uslugio:
                    return
                if self.total_person != len(m.out_phone_number):
                    self.total_person = len(m.out_phone_number)
                    self.time_out = datetime.now() + timedelta(minutes=5)
                    # print(f"START TIME_OUT_THREAD {str(self.time_out)}")

                if datetime.now() > self.time_out:
                    self.time_out = datetime.now() + timedelta(minutes=5)
                    if self.driver is not None:
                        print(f"TIME_OUT_THREAD!")
                        self.driver.quit()
                time.sleep(5)

            except Exception as detail:
                print(f"ERROR tim_out_thread:", detail)
                print("Перезапускаем tim_out_thread")
                self.driver = None

                if m.parsing_uslugio:
                    return self.tim_out_thread()
                else:
                    return

        return

    def get_profile(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")

        # Disable CSS
        profile.set_preference('permissions.default.stylesheet', 2)
        # Disable images
        profile.set_preference('permissions.default.image', 2)
        # Disable Flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        options = webdriver.FirefoxOptions()

        # Показать браузер
        if not self.show_browser:
            # Не показываем веб браузер
            # webdriver.Firefox.
            options.add_argument('-headless')

        return [profile, options]

    def set_proxy(self, proxy=True, change=False, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):

        m: MainWindow.MainWindow
        m = self.mainWindow

        if proxy:
            if change or len(m.uslugio_verified_proxies) == 0:
                while len(m.uslugio_verified_proxies) == 0:
                    if not m.parsing_uslugio:
                        return
                    print(f"Ждем прокси...")
                    time.sleep(2)
                else:
                    print(f"Работаем через прокси: {m.uslugio_verified_proxies[0]}")
                    ssl_addr = m.uslugio_verified_proxies[0].split(':')[0]
                    ssl_port = int(m.uslugio_verified_proxies[0].split(':')[1])

                    m.uslugio_used_proxies.append(m.uslugio_verified_proxies[0])
                    m.uslugio_verified_proxies = m.uslugio_verified_proxies[1:]
                    m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
            else:
                ssl_addr = m.uslugio_verified_proxies[0].split(':')[0]
                ssl_port = int(m.uslugio_verified_proxies[0].split(':')[1])

        self.driver.execute("SET_CONTEXT", {"context": "chrome"})

        try:
            self.driver.execute_script("""
              Services.prefs.setIntPref('network.proxy.type', 1);
              Services.prefs.setCharPref("network.proxy.http", arguments[0]);
              Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
              Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
              Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
              Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
              Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
              """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)

        finally:
            self.driver.execute("SET_CONTEXT", {"context": "content"})


class Execute(StartDriver):
    def __init__(self, mainWindow=None, url='', proxy=None, browser=False, js=''):
        super().__init__(mainWindow=mainWindow, url=url, proxy=proxy, browser=browser)
        self.mainWindow = mainWindow
        self.count_recurs = 0
        self.js = js

    # Добавляем на страницу свою библиотеку js
    def set_library(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        if not m.parsing_uslugio:
            return

        try:
            # Считываем скрипты
            library_js = open(self.js, 'r', encoding='utf-8').read()

            # Устанавливаем в нутри <body> последним элемент <script> </script> </body>
            # time.sleep(5)  # Останавливаем дальнейшее выполнения кода на 5 секунд

            # Внедряем скрирт set_library(data) в веб страницу
            self.driver.execute_script("""      
                script_set_library = function set_library(data) {
                        if ($('body').length != 0) {
                            var scr = document.createElement('script');
                            scr.textContent = data;
                            document.body.appendChild(scr);

                            return true;
                        }
                            return false;
                        }

                var scr = document.createElement('script');
                scr.textContent = script_set_library;
                document.body.appendChild(scr);
                
                script_check_function = function check_function(array){
                            var data = [];
                            for (var i = 0; i < array.length; i++) {
                                if (new Function('return typeof ' + array[i])() !== 'undefined') {
                                    console.log('Функция с именем ' + array[i] + ' существует!')
                                }
                                else{
                                    console.log('Функция с именем ' + array[i] + 'НЕ СУЩЕСТВУЕТ!')
                                    data.push(array[i]);
                                }
                            }
                            return data;
                        }
                
                scr = document.createElement('script');
                scr.textContent = script_check_function;
                document.body.appendChild(scr);
                
                if (!window.jQuery){
                    scr = document.createElement('script');
                    scr.type = 'text/javascript';
                    scr.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
                    document.head.appendChild(scr);
                }
            """)

            # Запускаем ранее внедренный скрипт set_library(data)
            self.execute_js(tr=1, sl=1, data=f"set_library({[library_js]})")

            data = re.findall(r'function\s+(\w+)[(]', library_js)
            js_functions = self.execute_js(tr=0, sl=1, rt=True, data=f"check_function({data})")

            if type(js_functions) == list and len(js_functions) > 0:
                for i in js_functions:
                    print(f"Не найден {i}")
                raise Exception("Не все скрепты были внедрены на вебстраницу!")
            print(f"Все скрипты установлены")

            return True

        except FileNotFoundError:
            print(f'Файл скрипты не найден {self.js}')
            return False

        except Exception as detail:
            print("ERROR set_library:", detail)
            if m.parsing_uslugio:
                return self.star_driver(url=self.set_url)
            else:
                return

    # js_execute запускает внедренные скрипты на странице и получает от них ответ
    def execute_js(self, tr=0, sl=0, rt=False, t=0, exit_loop=False, data=None):
        """
        :param tr: int Количество рекурсией (количество попыток найти элемент)
        :param sl: int Количество секунд ожидать перед выполнения кода
        :param rt: Если параметр rt = True то возвращам полученый от скрипта значение
        :param t: Если элемент не найден то вернуть: 0 - Данных нет; 1 - 0; 2 - False;
        :param exit_loop: Если метод вызван внутри цикла то exit_loop=True завершит цикл
        :param data: Название скрипта
        :return: Возвращает ответ если rt=True
        """
        m: MainWindow.MainWindow
        m = self.mainWindow

        if sl > 0:
            time.sleep(sl)  # Засыпаем

        try:
            # Запускаем javaScript в браузере и получаем результат
            result = self.driver.execute_script(f"return {data}")
        except Exception as detail:
            if not m.parsing_uslugio:
                return
            print(f"EXCEPT execute_js: {data}")
            print("ERROR:", detail)
            if exit_loop:
                print("ERROR:", detail)
                return 'not execute'
            else:
                return self.star_driver(url=self.set_url)  # Рекурсия с темеже параметрами

        # Если результа False и count_recurs < tr засыпаем на 2 сек. и запускаем рекурсию (рекурсия на случие если элемент не успел появится)
        if not result and self.count_recurs < tr:
            self.count_recurs += 1  # Увеличиваем счетчик рекурсии на +1
            return self.execute_js(tr=tr, sl=sl, rt=rt, t=t, exit_loop=exit_loop, data=data)  # Рекурсия с темеже параметрами

        # Результат False то возвращам по условию значение (Данных нет, 0, False)
        if not result:
            if t == 0:
                result = 'Данных нет'
            if t == 1:
                result = 0
            if t == 2:
                result = False

        # Обнуляем счетчик количество рекурсии
        self.count_recurs = 0

        # Если параметр rt = True то возвращам полученый от скрипта значение
        if rt:
            return result
