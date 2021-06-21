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

    def start_parsing_uslugio(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        u: UslugioParsing.UslugioThreading
        u = self.uslugioThreading

        try:
            while not self.stop_parsing:
                if not m.parsing_uslugio:
                    return

                show_more = 10
                while show_more > 0:
                    if not m.parsing_uslugio:
                        return
                    # Отображаем всех клиентов
                    show_more = self.execute_js(rt=True, t=2, exit_loop=True, data='show_more()')
                    # Проверяем выполнился ли скрипт
                    if show_more == 'not execute':
                        return self.up_date()  # Перезагружаем страницу
                    time.sleep(1)

                # Имена и услуги
                name_and_service = self.execute_js(rt=True, t=2, exit_loop=True, data='name_and_service()')
                # Проверяем выполнился ли скрипт
                if name_and_service == 'not execute':
                    return self.up_date()  # Перезагружаем страницу
                total = len(name_and_service[1])

                if m.uslugio_index == 0:
                    print(f"По ключевому слову {u.key_word} найдено: {total}")

                for i in range(0, total):
                    for retry in range(0, 10):
                        if not m.parsing_uslugio:
                            return

                        if name_and_service[1][i] not in m.out_service:
                            # Показываем клиента
                            open_item = self.execute_js(sl=2, rt=True, t=2, exit_loop=True, data=f"open_item({i})")
                            # Проверяем выполнился ли скрипт
                            if open_item == 'not execute':
                                if retry <= 4:
                                    continue
                                return self.up_date()  # Перезагружаем страницу


                            self.set_proxy(proxy=True, change=False)

                            if open_item:
                                # Номер телефона
                                phone = self.execute_js(tr=20, sl=3, rt=True, t=2, exit_loop=False, data=f"get_phone()")
                                # Проверяем выполнился ли скрипт или если вернул False
                                if 'not execute' == phone or not phone or 'error' == phone:
                                    if retry <= 4:
                                        m.uslugio_verified_proxies = m.uslugio_verified_proxies[1:]
                                        m.Commun.uslugio_proxy_update.emit(m.uslugio_verified_proxies)
                                        continue
                                    return self.up_date()  # Перезагружаем страницу

                                m.out_phone_number.append(phone)

                                # Имя
                                m.out_full_name.append(name_and_service[0][i])

                                # Услуги
                                m.out_service.append(name_and_service[1][i])

                                # Город
                                m.out_city.append(m.inp_city)

                                # key_word
                                m.out_key_word.append(u.key_word)

                                m.out_uslugio_all_data.append([m.out_full_name[-1], m.out_service[-1], m.out_phone_number[-1], m.out_key_word[-1],  m.out_city[-1]])
                                print(f"{len(m.out_service)}. {m.out_full_name[-1]}, {m.out_service[-1]}, {phone}, {m.out_key_word[-1]}")

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

                            if not m.parsing_uslugio:
                                return
                            # Посылаем сигнал на главное окно в прогресс бар uslugio
                            m.Commun.uslugio_progressBar.emit({'i': i, 'items': total})
                            break

                # Если все спарсино по ключевому слову то закрываем драйвер
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

            if not m.parsing_uslugio:
                return

            print(f"Перезагрузка driver с новым прокси {u.url}")

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