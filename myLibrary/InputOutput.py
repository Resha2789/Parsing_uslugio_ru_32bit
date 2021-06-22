# Входные данные
class IntPut:
    # Веб сайт
    inp_website = 'Uslugio'
    # Город
    inp_city = 'Уфа'
    # Ключевые слова
    inp_key_words = ['ЛВС', 'wifi']
    # Показывать браузер
    inp_show_browser = True
    # Прокси сервера
    inp_proxy = []
    # Файл Excel uslugio
    inp_name_excel_uslugio = ''
    # Дирриктория файла Excel uslugio
    inp_path_excel_uslugio = ''
    # Продолжить запись в файла
    inp_continuation_uslugio = True
    # Перезапись файла
    inp_rewriting_uslugio = False
    # Данные с сайта https://advanced.name/ru
    inp_auto_get_proxy = True
    # Данные вручную указываем откуда брать
    inp_manual_get_proxy = False
    # Сайт указанный вручную для получения прокси
    inp_path_manual_proxy = False


# Возвращаемые данные
class OutPut:
    # ФИО
    out_full_name = []
    # Почта
    out_email = []
    # Город
    out_city = []
    # Номер телефона
    out_phone_number = []
    # Услуги
    out_service = []
    # Ключевое слово
    out_key_word = []
    # Все данные
    out_uslugio_all_data = []
