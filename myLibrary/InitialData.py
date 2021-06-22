import json
import re
from myLibrary import InputOutput


class InitialData(InputOutput.IntPut, InputOutput.OutPut):
    def __init__(self):
        self.md = {
            'Город': 'Уфа',
            'Ключевые_слова': [],
            'Показывать_браузер': True,
            'Прокси_сервера': [],
            'Размер_окна': [600, 300],
            'Расположение_окна': [0, 0],
        }
        self.key_words_str = ''
        self.proxy_str = ''

    # Считываем данных с setting.txt
    def load_md(self):
        try:
            self.md = json.load(open('Все для сборщика данных/setting.txt'))
            print(f"Данные setting загружены {self.md}")
            self.inp_city = self.md['Город']
            self.inp_key_words = self.md['Ключевые_слова']
            self.inp_show_browser = self.md['Показывать_браузер']
            self.inp_proxy = self.md['Прокси_сервера']
            self.inp_path_excel_uslugio = self.md['Path_excel_uslugio']
            self.inp_name_excel_uslugio = self.md['Name_excel_uslugio']
            self.inp_continuation_uslugio = self.md['Продолжить_файл_uslugio']
            self.inp_rewriting_uslugio = self.md['Перезапись_файла_uslugio']

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

            # Статус парсинга uslugio
            self.parsing_uslugio = False

            # Найденные прокси сервера
            self.uslugio_proxy_finded = []

            # Проверенные прокси для uslugio
            self.uslugio_verified_proxies = []

            # Использованные прокси uslugio
            self.uslugio_used_proxies = []

            # Прокси сервера на вылет
            self.uslugio_index = 0

            # Стату поиска прокси для uslugio
            self.uslugio_found_proxy = False

        except Exception as error:
            self.update_json()
            print(f"Данных нет, созданы данные по умолчанию: {self.md}")

    # Обнавляем данные в setting.txt
    def update_json(self):
        self.md['Город'] = self.inp_city
        self.md['Ключевые_слова'] = self.inp_key_words
        self.md['Показывать_браузер'] = self.inp_show_browser
        self.md['Прокси_сервера'] = []
        self.md['Path_excel_uslugio'] = self.inp_path_excel_uslugio
        self.md['Name_excel_uslugio'] = self.inp_name_excel_uslugio
        self.md['Продолжить_файл_uslugio'] = self.inp_continuation_uslugio
        self.md['Перезапись_файла_uslugio'] = self.inp_rewriting_uslugio

        temp_md = {}
        temp_md.update(self.md)
        setting_json = open('Все для сборщика данных/setting.txt', 'w')
        json.dump(temp_md, setting_json, sort_keys=True, indent=4, ensure_ascii=False)
        setting_json.close()
