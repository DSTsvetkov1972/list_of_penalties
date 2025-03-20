from PySide6 import QtCore, QtWidgets
from colorama import Fore
from my_functions.dwh import execute_sql_click, insert_from_df, get_df_of_click
from my_functions.main_window import translit, load_file_sheet_name
import global_vars
import os
from datetime import datetime
from win32com.shell import shell, shellcon

class LoadInDWHThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)


    def run(self):
        load_file_sheet_name()
        global_vars.ui.footer_label.setStyleSheet('color: blue')
        global_vars.ui.footer_label.setText(f"Подготавливаем данные к загрузке в DWH...") 

        rows_number_column_name = 'Строка в исходнике'            
   
            

        #df_to_Insert = preprocessing(global_vars.df, global_vars.header_row, global_vars.horizontal_headers, global_vars.column_formats, rows_number_column_name)

        global_vars.ui.footer_label.setStyleSheet('color: blue')        
        global_vars.ui.footer_label.setText(f"Создаём таблицу {global_vars.dwh_table_name} в DWH...") 
        

 
        sql = f'''CREATE OR REPLACE TABLE {global_vars.dwh_table_name}
              (`Ст. Отправления` String,
              `Ст. Назначения` String,
              `№ Вагона` String,
              `№ контейнера` String,
              `№ контейнера (проверенный)` String,              
              `Тип контейнера` String,
              `№ накладной` String,
              `Наименование груза` String,
              `Дата отправки` String,
              `Дата отправки (проверенная)` DateTime Null)
              ENGINE = Memory()
              '''
        global_vars.ui.footer_label.setText(f"Шаг 0 из 3. Создаём таблицу в базе данных {global_vars.dwh_table_name}") 
        execute_sql_click(sql, operation_name = 'Создаём таблицу в базе данных')
        global_vars.ui.footer_label.setStyleSheet('color: blue')            
        global_vars.ui.footer_label.setText(f"Шаг 1 из 4. Загружаем в таблицу {global_vars.dwh_table_name} данные из файла...")   
        
        insert_from_df(global_vars.dwh_table_name,
                        global_vars.df_to_insert,
                        operation_name = f'Загружаем данные в таблицу {global_vars.dwh_table_name}')
        
        from sql.sql import sql
        global_vars.ui.footer_label.setStyleSheet('color: blue')            
        global_vars.ui.footer_label.setText("Шаг 2 из 4. Подтягиваем данные из DWH...")         
        df = get_df_of_click(sql(global_vars.dwh_table_name))   
        global_vars.ui.footer_label.setText("Шаг 3 из 4. Форматируем колонки...")   
        df['всего_строк'] = df['всего_строк'].apply(int)
        df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_01'] = df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_01'].apply(float)
        df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_01'] = df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_01'].apply(float)
        df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_02'] = df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_02'].apply(float)
        df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_02'] = df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_02'].apply(float)
        df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_04'] = df['RKS_RZD_amount_in_rub_without_vat_sum_0_01_01_04'].apply(float)
        df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_04'] = df['RKS_RZD_amount_in_contract_currency_without_vat_sum_0_01_01_04'].apply(float)
        df['RKS_RZD_amount_in_rub_without_vat_sum_2_01_01_01'] = df['RKS_RZD_amount_in_rub_without_vat_sum_2_01_01_01'].apply(float)
        df['RKS_RZD_amount_in_contract_currency_without_vat_sum_2_01_01_01'] = df['RKS_RZD_amount_in_contract_currency_without_vat_sum_2_01_01_01'].apply(float)
        #df['RKS_BEFORE_date_diff'] = df['RKS_BEFORE_date_diff'].apply(int)
        df['RKS_BEFORE_Date_E'] = df['RKS_BEFORE_Date_E'].apply(lambda d: None if d.strftime('%Y-%m-%d %H:%M:%S') == '1970-01-01 03:00:00' else d)
        df['RKS_BEFORE_amount_in_rub_without_vat_sum'] = df['RKS_BEFORE_amount_in_rub_without_vat_sum'].apply(lambda s: None if str(s)[0]=='0' else float(s))
        df['RKS_BEFORE_amount_in_contract_currency_without_vat_sum'] = df['RKS_BEFORE_amount_in_contract_currency_without_vat_sum'].apply(lambda s: None if str(s)[0]=='0' else float(s))
        #df['RKS_AFTER_date_diff'] = df['RKS_AFTER_date_diff'].apply(int)
        df['RKS_AFTER_Date_E'] = df['RKS_AFTER_Date_E'].apply(lambda d: None if d.strftime('%Y-%m-%d %H:%M:%S') == '1970-01-01 03:00:00' else d)        
        df['RKS_AFTER_amount_in_rub_without_vat_sum'] = df['RKS_AFTER_amount_in_rub_without_vat_sum'].apply(lambda s: None if str(s)[0]=='0' else float(s))
        df['RKS_AFTER_amount_in_contract_currency_without_vat_sum'] = df['RKS_AFTER_amount_in_contract_currency_without_vat_sum'].apply(lambda s: None if str(s)[0]=='0' else float(s))
        #print(Fore.MAGENTA, df[['RKS_BEFORE_date_diff','RKS_BEFORE_amount_in_rub_without_vat_sum']], Fore.WHITE)

        global_vars.ui.footer_label.setStyleSheet('color: blue')            
        global_vars.ui.footer_label.setText("Шаг 4 из 4. Записываем результат в файл Эксель...")

        # res_file_name = os.path.join(shell.SHGetKnownFolderPath(shellcon.FOLDERID_Downloads),f'unauthorized_seuizer_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv')
        res_file_name = os.path.join(shell.SHGetKnownFolderPath(shellcon.FOLDERID_Downloads),f'unauthorized_seuizer_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
        
        print(f'Стартовала запись датафрейма в Эксель-файл. df.memory_usage {df.memory_usage().sum()}')

        try: # df.memory_usage().sum() <= 200000000 :
            df.to_excel(res_file_name, index=False)
            print('Файл записан. Открываем...')
            os.startfile(res_file_name)
            global_vars.ui.footer_label.setStyleSheet('color: green')            
            global_vars.ui.footer_label.setText(f"Результат сохранен в {res_file_name}")
        except:
            global_vars.ui.footer_label.setStyleSheet('color: red')            
            global_vars.ui.footer_label.setText(f"Файл слишком большой. Попробуйте разделить его и обработать по частям")
   
        # print(global_vars.dwh_table_name)
        execute_sql_click(f"DROP TABLE IF EXISTS {global_vars.dwh_table_name}", operation_name = 'Удаляем временную таблицу')


        


    def on_started(self): # Вызывается при запуске потока
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)        
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False) 
        global_vars.ui.footer_text.setVisible(False)          
        


    def on_finished(self): # Вызывается при завершении потока
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(True)
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(True)
        global_vars.ui.comboSheets.setEnabled(True)
