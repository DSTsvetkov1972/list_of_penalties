global file                     # global_vars.file                     Путь к файлу информацию из которого нужно загрузить
global loaded_file              # global_vars.loaded_file              Путь к файлу информация из которого загружена в global_vars.df (т.е. когда мы определились, что именно этот файл хотим загрузить)
global sheet_names              # global_vars.sheet_names              Список листов в книге эксель, которую нужно загрузить
global sheet_name               # global_vars.sheet_name
global loaded_sheet_name        # global_vars.loaded_sheet_name        Имя листа инфораммция с которого загружеан в df
global df                       # global_vars.df                       Информация с листа загруженная в датафрейм  
global ui                       # global_vars.ui                       Главное окно программы. В глобальной переменной для доступности элементво интерфейса из всех потоков 
global header_row               # global_vars.header_row               Строка листа содержащая заголовки
global horizontal_headers       # global_vars.horizontal_headers       Заголовки
global column_formats           # global_vars.column_formats           Список объектов combobox из строки форматов 
global can_load_file            # global_vars.can_load_file            True если данные в поддерживаемом формате
global checks_dict              # global_vars.checks_dict              Атавизм. Возник при попытке сделать проверку форматов в нескольких потоках. Но работало как-то уж очень не красиво.
#global load_sheet_thread        # global_vars.load_sheet_thread
global check_result_style_sheet # global_vars.check_result_style_sheet Цвет combobox по результатам проверки
global log_in_status            # global_vars.log_in_status

global equipments_docs_df

checks_dict = {}

# version = '2024-09-19'
prog_name = "Перечень штрафников по ПИ"
version = '2025-хх-хх'

sample_columns = ['№ контейнера', 'Подкод перевозки'] # список колонок, который должен присутствовать в таблице ЦТЛ

dev_info = """Приложение работает не так как ожидалось?
Есть идеи что добавить или улучшить?
Хотите угостить разработчиков кофе?
Всегда рады будем с Вами пообщаться!
E-mail: TsvetkovDS@trcont.ru
моб. +7-903-617-77-55"""

manual = """Обращайтесь лично - объясню на словах, так быстрее и понятнее )"""