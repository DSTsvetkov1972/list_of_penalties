global file                     # Путь к файлу информацию из которого нужно загрузить
global loaded_file              # Путь к файлу информация из которого загружена в global_vars.df (т.е. когда мы определились, что именно этот файл хотим загрузить)
global sheet_names              # Список листов в книге эксель, которую нужно загрузить
global sheet_name               # global_vars.sheet_name
global loaded_sheet_name        # Имя листа инфораммция с которого загружеан в df
global df                       # Информация с листа загруженная в датафрейм  
global ui                       # Главное окно программы. В глобальной переменной для доступности элементво интерфейса из всех потоков 
global header_row               # Строка листа содержащая заголовки
global horizontal_headers       # Заголовки
global column_formats           # Список объектов combobox из строки форматов 
global can_load_file            # True если данные в поддерживаемом формате
global check_result_style_sheet # global_vars.check_result_style_sheet Цвет combobox по результатам проверки
global log_in_status            # global_vars.log_in_status
global equipments_docs_df



