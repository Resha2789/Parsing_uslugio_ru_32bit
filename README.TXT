Компеляция в .exe
pyinstaller --onefile --noconsole --distpath D:\Фриланс\Авито\None\ -n Сборщик Main.py
pyinstaller --onefile --noconsole --icon "D:\Programming\Python\Parsing_uslugio_ru_64bit\Все для сборщика данных\icon_phone.ico" --distpath D:\Фриланс\Авито\Сборщик_данных_uslugio_64bit\ -n Сборщик_телефонов_64bit Main.py
pyinstaller --onefile --icon "D:\Programming\Python\Parsing_uslugio_ru_64bit\Все для сборщика данных\icon_phone.ico" --distpath D:\Фриланс\Авито\Сборщик_данных_uslugio_64bit\ -n Сборщик_телефонов_64bit Main.py

--hidden-import pywinauto

Конвертация ui в py
pyuic5 D:\Programming\Python\Goblin_drilling_v.2.2\Lib\site-packages\QtDesigner\Uslugio_avito_parsing.ui -o myLibrary\My_pyqt5\Uslugio_avito_parsing.py

В библиотеке venv/Lib/site-packages/selenium/webdriver/common/service.py
изменил строку 77 добавил аргумент в subprocess.Popen add (shell = True) что бы не показывать консоли geckodriver

Используемые библиотеки
DAWG-Python	0.7.2	0.7.2
PyQt5	5.15.4	5.15.4
PyQt5-Qt5	5.15.2	5.15.2
PyQt5-sip	12.9.0	12.9.0
Unidecode	1.2.0	1.2.0
altgraph	0.17	0.17
beautifulsoup4	4.9.3	4.9.3
bs4	0.0.1	0.0.1
certifi	2021.5.30	2021.5.30
chardet	4.0.0	4.0.0
colorama	0.4.4	0.4.4
comtypes	1.1.10	1.1.10
configparser	5.0.2	5.0.2
crayons	0.4.0	0.4.0
docopt	0.6.2	0.6.2
et-xmlfile	1.1.0	1.1.0
future	0.18.2	0.18.2
idna	2.10	3.2
keyboard	0.13.5	0.13.5
lxml	4.6.3	4.6.3
numpy	1.20.3	1.21.0
packaging	20.9	20.9
pefile	2021.5.24	2021.5.24
pip	21.1.2	21.1.2
psutil	5.8.0	5.8.0
pyinstaller	4.3	4.3
pyinstaller-hooks-contrib	2021.1	2021.1
pymorphy2	0.9.1	0.9.1
pymorphy2-dicts-ru	2.4.417127.4579844	2.4.417127.4579844
pyparsing	2.4.7	2.4.7
python-dateutil	2.8.1	2.8.1
pytz	2021.1	2021.1
pywin32	301	301
pywin32-ctypes	0.2.0	0.2.0
requests	2.25.1	2.25.1
selenium	3.141.0	3.141.0
setuptools	57.0.0	57.0.0
sip	6.1.1
six	1.16.0	1.16.0
soupsieve	2.2.1
toml	0.10.2
urllib3	1.26.5