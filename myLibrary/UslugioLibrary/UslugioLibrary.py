from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from myLibrary import InitialData, InputOutput
from myLibrary import ProxyCheck
import time
import re


# Чтения из Excel (входные параметры)
class ReadData(InitialData.InitialData):
    def __init__(self):
        super().__init__()
        self.key_words_str = ''
        self.proxy_str = ''

    def read_data(self):
        self.load_md()

        # Ключевые слова
        self.key_words_str = ''
        for i in self.inp_key_words:
            self.key_words_str += i + ', '
        if len(self.key_words_str) > 0:
            self.key_words_str = re.sub(r'(,\s)$', '', self.key_words_str)

        # Прокси сервера
        self.proxy_str = ''
        for i in self.inp_proxy:
            self.proxy_str += i + '\n'

        return True


# Запуск WebDriverChrome
class StartDriver(ReadData, ProxyCheck.ProxyCheck):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.proxy = None

    def star_driver(self):
        # Устанавливаем опции для webdriverChrome
        options = webdriver.ChromeOptions()
        # Развернуть на весь экран
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Утсанавливаем запрет на загрузку изоброжении
        # options.add_argument('--blink-settings=imagesEnabled=false')
        if self.proxy is None:
            self.proxy = []
            for i in self.inp_proxy:
                self.proxy.append(i)

        if self.proxy is not None:
            for i in self.proxy:
                if self.proxy_check('https://uslugio.com/', i):
                    options.add_argument('--proxy-server=%s' % i)
                    self.proxy = self.proxy[1:]
                    break
                self.proxy = self.proxy[1:]

        # Если опция Браузер: Скрыть
        if not self.inp_show_browser:
            # Не показываем веб браузер
            options.add_argument('headless')

        # Запускаем webDriverChrome

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'})

        return True


class UrlUslugio(StartDriver):
    def __init__(self):
        super().__init__()
        self.link = None
        self.index = 0

    def create_url_uslugio(self):
        # Формируем url ссылку с выбранными параметрами
        self.link = f"https://uslugio.com/{self.inp_city}?search={self.inp_key_words[self.index]}"

        # Загружаем сайт по ссылке link
        self.driver.get(self.link)

        return True


class Execute(UrlUslugio, InputOutput.OutPut):
    def __init__(self):
        super().__init__()
        self.count_recurs = 0

    # Добавляем на страницу свою библиотеку js
    def set_library(self):
        try:
            # Считываем скрипты
            library_js = open('myLibrary/JsLibrary/UslugioJsLibrary.js', 'r', encoding='utf-8').read()

            # Устанавливаем в нутри <body> последним элемент <script> </script> </body>
            time.sleep(5)  # Останавливаем дальнейшее выполнения кода на 5 секунд

            # Внедряем скрирт set_library(data) в веб страницу
            self.driver.execute_script("""      
                script = function set_library(data) {
                        if ($('body').length != 0) {
                            var scr = document.createElement('script');
                            scr.textContent = data;
                            document.body.appendChild(scr);
                            return true;
                        }
                            return false;
                        }

                var scr = document.createElement('script');
                scr.textContent = script;
                document.body.appendChild(scr);
            """)

            # Запускаем ранее внедренный скрипт set_library(data)
            self.execute_js(tr=1, data=f"set_library({[library_js]})")

            return True

        except FileNotFoundError:
            print('Файл libraryJs.js не найден.')
            return False

    # js_execute запускает внедренные скрипты на странице и получает от них ответ
    def execute_js(self, tr=0, sl=0, rt=False, t=0, data=None):
        """
        :param tr: int Количество рекурсией (количество попыток найти элемент)
        :param sl: int Количество секунд ожидать перед выполнения кода
        :param rt: Если параметр rt = True то возвращам полученый от скрипта значение
        :param t: Если элемент не найден то вернуть: 0 - Данных нет; 1 - 0; 2 - False;
        :param data: Название скрипта
        :return: Возвращает ответ если rt=True
        """
        if sl > 0:
            time.sleep(sl)  # Засыпаем

        # Запускаем javaScript в браузере и получаем результат
        result = self.driver.execute_script(f"return {data}")

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


class Update(Execute):
    def __init__(self):
        super().__init__()

    def up_date(self, parent, item):
        # Закрываем драйвер Chrome
        self.driver.close()

        # Запус WebDriverChrome
        if not self.star_driver():
            return
        # Формируем url ссылку с входными параметрами
        if not self.create_url_uslugio():
            return
        # Устанавливаем на вебсайт скрипты
        if not self.set_library():
            return
        # Запускаем цикл парсинга uslugio
        parent.start_parsing_uslugio(index=item)


class ParsingUslugio(Update, Execute):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        super(ParsingUslugio, self).__init__()
        self.stop_parsing = False
        self.pause_parsing = False

    def start_parsing_uslugio(self, index=0):
        while not self.stop_parsing:

            # Отображаем всех клиентов
            while self.execute_js(rt=True, t=2, data='show_more()') > 0:
                time.sleep(1)

            # Количество клиентов
            items = self.execute_js(rt=True, t=1, data='count_items()')
            print(f"Работает {self.inp_website}, найдено: {items}")

            counter = 0
            for i in range(index, items):
                # Скроллинг на клиента
                self.execute_js(tr=2, sl=1, rt=False, t=2, data=f"scroll_item({i})")

                # Показываем клиента
                if self.execute_js(sl=1, rt=True, t=2, data=f"open_item({i})"):
                    # Скроллинг на телефон
                    self.execute_js(tr=2, sl=1, rt=False, t=2, data=f"scroll_phone()")

                    # Номер телефона
                    phone = self.execute_js(tr=2, sl=1, rt=True, t=2, data=f"get_phone()")
                    self.out_phone_number.append(phone)

                    # Имя
                    name = self.execute_js(tr=2, sl=1, rt=True, t=2, data=f"name()")
                    self.out_full_name.append(name)

                    # Город
                    self.out_city.append(self.inp_city)

                    # Услуги
                    self.out_service.append(self.inp_key_words[-1])

                    print(f"{i + 1}. Имя: {name}, город: {self.inp_city}, тел. {phone}, услуги: {self.out_service[-1]}")

                    # Выходим назад к клиентам
                    self.execute_js(tr=0, sl=1, rt=False, t=2, data=f"back()")

                    # Стоп парсинг
                    if self.stop_parsing:
                        print(f"Парсинг остановлен {self.inp_website}")
                        print(f"Спарсено {len(self.out_phone_number)}")
                        break

                    # Парсинг на паузу
                    show_data = True
                    while self.pause_parsing:
                        if show_data:
                            print(f"Парсинг на паузе {self.inp_website}")
                            print(f"Спарсено {len(self.out_phone_number)}")
                            show_data = False
                        time.sleep(1)

                    if phone == 'error':
                        return self.up_date(self, i)

                # Посылаем сигнал на главное окно в прогресс бар uslugio
                self.mainWindow.Commun.uslugio_progressBar.emit({'i': i, 'items': items})

            return
