from myLibrary import DriverChrome
from myLibrary import MainWindow
from myLibrary.UslugioLibrary import UslugioParsing
import time
import re


# self, mainWindow=None, proxy=None, browser=False, url='', js=''
# url=url, proxy=proxy, browser=browser, js=js

class ParsingUslugio(DriverChrome.Execute):
    def __init__(self, mainWindow=None, uslugioThreading=None, *args, **kwargs):
        super(ParsingUslugio, self).__init__(mainWindow=mainWindow, *args, **kwargs)
        self.mainWindow = mainWindow
        self.uslugioThreading = uslugioThreading
        self.stop_parsing = False
        self.pause_parsing = False
        self.item = 0
        self.total = 5

    def start_parsing_uslugio(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        u: UslugioParsing.UslugioThreading
        u = self.uslugioThreading

        try:
            while not self.stop_parsing:

                show_more = 10
                while show_more > 0:
                    # Отображаем всех клиентов
                    show_more = self.execute_js(rt=True, t=2, exit_loop=True, data='show_more()')
                    # Проверяем выполнился ли скрипт
                    if show_more == 'not execute':
                        return self.up_date()  # Перезагружаем страницу
                    time.sleep(1)

                # Количество клиентов
                items = self.execute_js(rt=True, t=1, exit_loop=True, data='count_items()')
                # Проверяем выполнился ли скрипт
                if items == 'not execute':
                    return self.up_date()  # Перезагружаем страницу

                if m.uslugio_index_item == 0:
                    print(f"Найдено: {items}")
                else:
                    print(f"Осталось: {items - (m.uslugio_index_item + 1)}")

                for i in range(m.uslugio_index_item, items):

                    # Показываем клиента
                    open_item = self.execute_js(sl=2, rt=True, t=2, exit_loop=True, data=f"open_item({i})")
                    # Проверяем выполнился ли скрипт
                    if open_item == 'not execute':
                        return self.up_date()  # Перезагружаем страницу
                    if open_item:
                        # Номер телефона
                        phone = self.execute_js(tr=10, sl=1, rt=True, t=2, exit_loop=True, data=f"get_phone()")
                        # Проверяем выполнился ли скрипт или если вернул False
                        if 'not execute' == phone or not phone or 'error' == phone:
                            m.uslugio_index_item = i
                            return self.up_date()
                        m.out_phone_number.append(phone)

                        # Имя
                        name = self.execute_js(tr=2, sl=0, rt=True, t=2, exit_loop=True, data=f"name()")
                        # Проверяем выполнился ли скрипт
                        if name == 'not execute':
                            return self.up_date()  # Перезагружаем страницу
                        m.out_full_name.append(name)

                        # Город
                        m.out_city.append(m.inp_city)

                        # Услуги
                        m.out_service.append(u.key_word)

                        print(f"{i + 1}. Имя: {name}, город: {m.inp_city}, тел. {phone}, услуги: {m.out_service[-1]}")

                        # Стоп парсинг
                        if self.stop_parsing:
                            print(f"Парсинг остановлен {m.inp_website}")
                            print(f"Спарсено {len(m.out_phone_number)}")
                            break

                        # Парсинг на паузу
                        show_data = True
                        while self.pause_parsing:
                            if show_data:
                                print(f"Парсинг на паузе {m.inp_website}")
                                print(f"Спарсено {len(m.out_phone_number)}")
                                show_data = False
                            time.sleep(1)

                    # Посылаем сигнал на главное окно в прогресс бар uslugio
                    m.Commun.uslugio_progressBar.emit({'i': i, 'items': items})

                # Если все спарсино по ключевому слову то закрываем драйвер
                m.uslugio_index_item = 0
                print(f"Все спарсино по ключевому слову {u.key_word}")
                return

        except Exception as detail:
            print(f"EXCEPT start_parsing_uslugio")
            print("ERROR:", detail)
            self.up_date()

    def up_date(self):
        try:
            m: MainWindow.MainWindow
            m = self.mainWindow

            u: UslugioParsing.UslugioThreading
            u = self.uslugioThreading

            print(f"Количество прокси {len(m.uslugio_proxy)}")
            if len(m.uslugio_proxy) == 0:
                m.uslugio_found_proxy = False
                m.start_uslugio_find_proxy()
                while not m.uslugio_found_proxy:
                    print(f"Ждем прокси...")
                    time.sleep(1)

            print(f"Перезагрузка с новым прокси {u.url}")

            # Запус WebDriverChrome
            if not self.star_driver(url=u.url):
                print(f"False star_driver")
                return
            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                print(f"False set_library")
                return

            # Запускаем цикл парсинга uslugio
            self.start_parsing_uslugio()

        except Exception as detail:
            print("ERROR up_date:", detail)
            print("Пробуем снова запустить up_date через 10 сек")
            time.sleep(10)
            return self.up_date()
