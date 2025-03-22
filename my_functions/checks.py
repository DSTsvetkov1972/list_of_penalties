import pandas as pd
import re
import time 

no_errs_df = pd.DataFrame(columns = ['column_number','Сообщение','Ячейка LN','Ячейка RNCN','Значение'])

def date_parser(date_str):
        patterns = ['%d-%m-%Y %H:%M:%S',
                    '%d-%m-%Y %H:%M',
                    '%d-%m-%Y',
                    '%d.%m.%Y %H:%M:%S',
                    '%d.%m.%Y %H:%M',
                    '%d.%m.%Y'
                    '%d.%m.%Y %H:%M:%S',
                    '%d.%m.%Y %H:%M',
                    '%d.%m.%Y',
                    '%Y-%m-%d %H:%M:%S.%f',                    
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%Y-%m-%d'                 
                    ]
                    
        for pattern in patterns:
            try:
                dt = time.strptime(date_str, pattern)
                result = f"{dt.tm_year}-{str(dt.tm_mon).zfill(2)}-{str(dt.tm_mday).zfill(2)} {str(dt.tm_hour).zfill(2)}:{str(dt.tm_min).zfill(2)}:{str(dt.tm_sec).zfill(2)}"
                return result
            except:
                pass
        return ''

def preprocess_datetime(df):
    df['Дата отправки (проверенная)'] = df['Дата отправки'].apply(date_parser)
    err_df = df[['Дата отправки','Дата отправки (проверенная)']][df['Дата отправки (проверенная)']=='']
    err_list = [('Дата отправки', err[0], err[1]) for err in err_df.itertuples()]
    return err_list

def container_parser(container_number):
        container_number = container_number.upper().replace('К', 'K').replace('Т','T').replace(' ','')
        pattern = re.compile(r'[A-Z]{4}\d{7}')

        if len(container_number) != 11 or re.match(pattern, container_number) is None:
            return ''
        else:
            return container_number

def preprocess_container(df):
    df['sent_number_equipment'] = df['№ контейнера'].apply(container_parser)
    err_df = df[['№ контейнера','sent_number_equipment']][df['sent_number_equipment']=='']
    err_list = [('№ контейнера', err[0], err[1]) for err in err_df.itertuples()]
    return err_list

def route_subcode_parser(route_subcode):
        """
        Подкод перевозки должен содержать в себе корректный номер заказа начиная с 4-ой позиции 
        """
        if len(route_subcode) != 12:
            return ''
        else:
            try:
                i = int(route_subcode[3:11])
            except ValueError:
                return ''
        if 13000000<=i<=80000000:
            return route_subcode[3:11]
        else:
             return ""

def preprocess_route_subcode(df):
    df['order_id'] = df['Подкод перевозки'].apply(route_subcode_parser)
    err_df = df[['Подкод перевозки','order_id']][df['order_id']=='']
    err_list = [('Подкод перевозки', err[0], err[1]) for err in err_df.itertuples()]
    return err_list

def header_checker(sample_columns:list, header_row:list )->list:
    """функция проверяет, чтобы таблица содержала нужные заголовки и
    чтобы заголовки не повторялись.
    Возвращает список недостающих и повторяющихся заголовков
    """

    err_list = []

    for column in sample_columns:
        if column not in header_row:
            err_list.append((column,'колонка отсутствует'))
        elif header_row.count(column) > 1:
            err_list.append((column,f'колонок с таким названием: {header_row.count(column)}'))


    return err_list    

if __name__ == '__main__':
    print(route_subcode_parser('630324317215'))
