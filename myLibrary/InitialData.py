import json
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

    # Считываем данных с setting.txt
    def load_md(self):
        try:
            self.md = json.load(open('myLibrary/setting.txt'))
            print(f"Данные setting загружены {self.md}")
            self.inp_city = self.md['Город']
            self.inp_key_words = self.md['Ключевые_слова']
            self.inp_show_browser = self.md['Показывать_браузер']
            self.inp_proxy = self.md['Прокси_сервера']


        except FileNotFoundError:
            self.update_json()
            print(f"Данных нет, созданы данные по умолчанию: {self.md}")

    # Обнавляем данные в setting.txt
    def update_json(self):
        self.md['Город'] = self.inp_city
        self.md['Ключевые_слова'] = self.inp_key_words
        self.md['Показывать_браузер'] = self.inp_show_browser
        self.md['Прокси_сервера'] = self.inp_proxy

        temp_md = {}
        temp_md.update(self.md)
        setting_json = open('myLibrary/setting.txt', 'w')
        json.dump(temp_md, setting_json, sort_keys=True, indent=4, ensure_ascii=False)
        setting_json.close()
