prog_name = "Перечень штрафников по ПИ"

version = '2025-03-25'

# Список параметров для передачи лицу ответственному за предоставление доступа к БД iSales-3
# для ПРОГРАММЫ СОЗДАНИЯ ФАЙЛА АУТЕНТИФИКАЦИИ (ПСФА)
params = ['host', 'dbname', 'user', 'password', 'port']

# описание для ПРОГРАММЫ СОЗДАНИЯ ФАЙЛА АУТЕНТИФИКАЦИИ (ПСФА)
description = '''Параметры подключения к БД iSales' \
    для утилиты отдела таможеного оформления list_of_penalties' \
    пользователь Леутин А.С'''

# список форматов исходного файла
file_formats_list = ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']

# список колонок, который должен присутствовать в таблице ЦТЛ
sample_columns = ['№ контейнера', 'Подкод перевозки'] 

# Текст контактов доступный через меню
dev_info = """Приложение работает не так как ожидалось?
Есть идеи что добавить или улучшить?
Хотите угостить разработчиков кофе?
Всегда рады будем с Вами пообщаться!
E-mail: TsvetkovDS@trcont.ru
моб. +7-903-617-77-55"""

# Текст инструкции доступной через меню
manual = """Обращайтесь лично - объясню на словах, так быстрее и понятнее )"""