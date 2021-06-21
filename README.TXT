Компеляция в .exe
pyinstaller --onefile --noconsole --distpath D:\Фриланс\Авито\None\ -n Сборщик Main.py
pyinstaller --onefile --noconsole --icon D:\Programming\Python\Parsing_Uslugio_Avito\icon_phone.ico --distpath D:\Фриланс\Авито\Неизвестный\ -n Сборщик_телефонов Main.py

Конвертация ui в py
pyuic5 D:\Programming\Python\Goblin_drilling_v.2.2\Lib\site-packages\QtDesigner\Uslugio_avito_parsing.ui -o myLibrary\My_pyqt5\Uslugio_avito_parsing.py

В библиотеке venv/Lib/site-packages/selenium/webdriver/common/service.py
изменил строку 77 добавил аргумент в subprocess.Popen add (shell = True) что бы не показывать консоли geckodriver

Используемые библиотеки
PyQt5	5.15.4	5.15.4
PyQt5-Qt5	5.15.2	5.15.2
PyQt5-sip	12.9.0	12.9.0
Unidecode	1.2.0	1.2.0
certifi	2021.5.30	2021.5.30
chardet	4.0.0	4.0.0
colorama	0.4.4	0.4.4
configparser	5.0.2	5.0.2
crayons	0.4.0	0.4.0
idna	2.10	3.2
keyboard	0.13.5	0.13.5
pip	21.1.2	21.1.2
requests	2.25.1	2.25.1
selenium	3.141.0	3.141.0
setuptools	57.0.0	57.0.0
urllib3	1.26.5	1.26.5
webdriver-manager	3.4.2	3.4.2