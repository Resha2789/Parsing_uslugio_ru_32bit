import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from myLibrary import ProxyCheck
from myLibrary import MainWindow
import time
import socket
import threading


# Запуск WebDriverChrome
# url='', proxy=None, browser=False
class StartDriver(ProxyCheck.ProxyCheck):
    def __init__(self, mainWindow=None, url='', proxy=None, browser=False):
        super().__init__()
        self.mainWindow = mainWindow
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.driver = None
        self.show_browser = browser
        self.loadStatus = False
        self.driver_closed = False
        self.set_url = url

    def star_driver(self, url=None, find_proxy=True):
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.set_url = url

        if self.driver is not None:
            try:
                print(f"DRIVER CLOSE")
                self.driver.close()
                time.sleep(4)
                self.driver = None
            except Exception as detail:
                self.driver = None
                print("ERROR DRIVER CLOSE:", detail)

        print(f"DRIVER START")
        # Устанавливаем опции для webdriverChrome
        options = webdriver.ChromeOptions()
        # Развернуть на весь экран
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Утсанавливаем запрет на загрузку изоброжении
        options.add_argument('--blink-settings=imagesEnabled=false')
        # Показать браузер
        if not self.show_browser:
            # Не показываем веб браузер
            options.add_argument('headless')

        if m.uslugio_proxy is not None:
            if not find_proxy:
                print(f"Опция proxy-server {m.uslugio_proxy[0]}")
                options.add_argument('--proxy-server=%s' % m.uslugio_proxy[0])
            else:
                for i in m.uslugio_proxy:
                    if self.proxy_check('https://uslugio.com/', i):
                        options.add_argument('--proxy-server=%s' % i)
                        m.uslugio_proxy = m.uslugio_proxy[1:]
                        break
                    m.uslugio_proxy = m.uslugio_proxy[1:]
                    if len(m.uslugio_proxy) == 0:
                        m.uslugio_found_proxy = False
                        m.start_uslugio_find_proxy()
                        while not m.uslugio_found_proxy:
                            print(f"Ждем прокси...")
                            time.sleep(1)
                        return self.star_driver(url=self.set_url)
        try:
            # Запускаем webDriverChrome
            socket.setdefaulttimeout(120)
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'})
            self.driver.set_page_load_timeout(120)

            # Загружаем сайт по ссылке url
            # threading.Thread(target=self.tim_out_thread).start()
            self.driver.get(url)
            # if self.driver_closed:
            #     print("Перезапускаем star_driver")
            #     return self.star_driver(url=url)

            self.loadStatus = True
            print("Заргузка страницы успешна прошла.")

        except Exception as detail:
            # self.driver_closed = False
            print("ERROR star_driver:", detail)
            print("Перезапускаем star_driver")
            return self.star_driver(url=self.set_url, find_proxy=find_proxy)

        return True

    # Thread
    def tim_out_thread(self):
        self.loadStatus = False
        print("started tim_out_thread")
        time.sleep(40)
        if not self.loadStatus:
            print("timeout первышен 40сек")
            self.driver_closed = True
            return


class Execute(StartDriver):
    def __init__(self, mainWindow=None, url='', proxy=None, browser=False, js=''):
        super().__init__(mainWindow=mainWindow, url=url, proxy=proxy, browser=browser)
        self.count_recurs = 0
        self.js = js

    # Добавляем на страницу свою библиотеку js
    def set_library(self):
        try:
            # Считываем скрипты
            library_js = open(self.js, 'r', encoding='utf-8').read()

            # Устанавливаем в нутри <body> последним элемент <script> </script> </body>
            time.sleep(5)  # Останавливаем дальнейшее выполнения кода на 5 секунд

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
            self.execute_js(tr=1, sl=3, data=f"set_library({[library_js]})")

            data = re.findall(r'function\s+(\w+)[(]', library_js)
            js_functions = self.execute_js(tr=0, sl=3, rt=True, data=f"check_function({data})")

            time.sleep(3)
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
            return self.star_driver(url=self.set_url)

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
        if sl > 0:
            time.sleep(sl)  # Засыпаем

        try:
            # Запускаем javaScript в браузере и получаем результат
            result = self.driver.execute_script(f"return {data}")
        except Exception as detail:
            print(f"EXCEPT execute_js: {data}")
            print("ERROR:", detail)
            if exit_loop:
                print("ERROR:", detail)
                return 'not execute'
            else:
                return self.star_driver(url=self.set_url)  # Рекурсия с темеже параметрами

        # Если результа False и count_recurs < tr засыпаем на 2 сек. и запускаем рекурсию (рекурсия на случие если элемент не успел появится)
        if not result and self.count_recurs < tr:
            time.sleep(2)
            self.count_recurs += 1  # Увеличиваем счетчик рекурсии на +1
            return self.execute_js(tr=tr, sl=0, rt=rt, t=t, data=data)  # Рекурсия с темеже параметрами

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
