from myLibrary.UslugioLibrary.UslugioLibrary import ParsingUslugio
from PyQt5.QtCore import QThread


class UslugioThreading(QThread, ParsingUslugio):
    def __init__(self, parent=None):
        super().__init__(mainWindow=parent)
        self.mainWindow = parent
        # print("\nВременная остановка парсинга 'Ctr + P'"
        #       "\nПродолжить парсинг 'Ctr + P'"
        #       "\nПолная остановка парсинга нажмите 'Ctr + S'\n")

    def run(self):
        # Чтение входных данных
        if not self.read_data():
            return
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
        self.start_parsing_uslugio()
        # Завершаем программу
        # self.close()
