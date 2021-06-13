from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from myLibrary import ProxyCheck
import time


# Запуск WebDriverChrome
class StartDriver(ProxyCheck.ProxyCheck):
    def __init__(self, proxy=None, browser=False, url=''):
        super().__init__()
        self.driver = None
        self.proxy = proxy
        self.show_browser = browser
        self.url = url

    def star_driver(self):
        # Устанавливаем опции для webdriverChrome
        options = webdriver.ChromeOptions()
        # Развернуть на весь экран
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Утсанавливаем запрет на загрузку изоброжении
        # options.add_argument('--blink-settings=imagesEnabled=false')
        if self.proxy is not None:
            for i in self.proxy:
                if self.proxy_check('https://uslugio.com/', i):
                    options.add_argument('--proxy-server=%s' % i)
                    break

        # Показать браузер
        if not self.show_browser:
            # Не показываем веб браузер
            options.add_argument('headless')

        # Запускаем webDriverChrome

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'})

        # Загружаем сайт по ссылке link
        self.driver.get(self.url)

        return True


class Execute(StartDriver):
    def __init__(self, url='', proxy=None, browser=False, js=''):
        super().__init__(url=url, proxy=proxy, browser=browser)
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
            print(f'Файл скрипты не найден {self.js}')
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
