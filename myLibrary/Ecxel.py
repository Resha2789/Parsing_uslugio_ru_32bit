from myLibrary import MainWindow
import pythoncom
import win32com.client


class ExcelWrite:
    def __init__(self, mainWindow=None):
        self.mainWindow = mainWindow
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.excel = None
        self.book = None
        self.sheet = None
        self.write_data = None
        self.read_data = None
        self.open_excel = False

    def load_work_book(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            if not self.open_excel:
                # Показываем что СОМ объект будет использовать в отдельном потоке
                # noinspection PyUnresolvedReferences
                pythoncom.CoInitialize()
                # Cоздадим COM объект
                self.excel = win32com.client.Dispatch("Excel.Application")

                if self.excel.Application.Workbooks.Count > 0:
                    if not self.set_property_excel():
                        return False

                    # Проверяем наличие открытого файла
                    for i in range(1, self.excel.Application.Workbooks.Count + 1):
                        if m.inp_name_excel_uslugio == self.excel.Application.Workbooks(i).Name:
                            self.book = self.excel.Application.Workbooks(i)
                            break

                if self.book == None:
                    self.book = self.excel.Workbooks.Open(m.inp_path_excel_uslugio)

                self.sheet = self.book.Sheets(1)
                self.open_excel = True
                print(f"open_excel {m.inp_name_excel_uslugio}")

            return True

        except Exception as error:
            self.open_excel = False
            print(f"load_work_book {error}")
            return False

    def set_property_excel(self):
        try:
            self.excel.Application.DisplayAlerts = False
            self.excel.Application.ScreenUpdating = True
            # self.Excel.Application.visible = True
            return True

        except Exception as error:
            print(f"set_property_excel {error}")
            return False

    def write_to_excel(self, data=None, row=0):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            self.sheet.Cells.ClearContents()
            for line in data:
                row += 1
                self.sheet.Range(self.sheet.Cells(row, 1), self.sheet.Cells(row, len(line))).Value = line

            self.exit_excel()
            print(f"Данные сохранились успешно {m.inp_name_excel_uslugio}")
            return True

        except Exception as error:
            print(f"write_to_excel {error}")
            print(f"Данные не сохранились (что-та пошло не так) {m.inp_name_excel_uslugio}")
            return False

    def read_from_excel(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        try:
            rows = int(self.excel.WorksheetFunction.CountA(self.excel.Columns(1)))
            data = self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(rows, 5)).Value

            row = 1
            m.out_service = []
            m.out_uslugio_all_data = []
            for i in data:
                # m.out_uslugio_all_data.append([m.out_full_name[-1], m.out_service[-1], m.out_phone_number[-1], m.out_key_word[-1],  m.out_city[-1]])
                if i[1] is None:
                    break

                m.out_service.append(i[1])
                m.out_uslugio_all_data.append([i[0], i[1], i[2], i[3], i[4]])

            print(f"Данные загрузились {m.inp_name_excel_uslugio}: {rows} строк")
            self.exit_excel()
            return True

        except Exception as error:
            print(f"read_from_excel {error}")
            print(f"Данные не загрузились (что-та пошло не так) {m.inp_name_excel_uslugio}")
            return False

    def exit_excel(self):
        self.excel.Application.DisplayAlerts = False
        self.excel.ScreenUpdating = True
        self.book.Save()
        self.book.Close()
        self.sheet = None
        self.book = None
        self.excel.Quit()
        self.excel = None