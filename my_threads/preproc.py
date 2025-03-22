from PySide6 import QtCore
import pandas as pd
import global_vars
from my_functions.main_window import fill_in_err_table, fill_in_table, load_file_sheet_name
from my_functions.checks import preprocess_route_subcode, preprocess_container
from colorama import Fore


class PreprocThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        load_file_sheet_name()

        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)  
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)                   
        global_vars.ui.err_tableWidget.setVisible(False) 

        
        global_vars.df_to_insert = global_vars.df.iloc[global_vars.header_row:]
        global_vars.df_to_insert.columns = list(global_vars.df.iloc[global_vars.header_row-1])
        #global_vars.df_to_insert = global_vars.df_to_insert[list(global_vars.sample_columns)]
        


        err_list = []
        
        global_vars.ui.footer_label.setStyleSheet('color: blue')             
        global_vars.ui.footer_label.setText(f"Проверяем столбец 'Подкод перевозки'")
        err_list += preprocess_route_subcode(global_vars.df_to_insert)

        global_vars.ui.footer_label.setStyleSheet('color: blue')             
        global_vars.ui.footer_label.setText(f"Проверяем столбец '№ контейнера'")        
        err_list += preprocess_container(global_vars.df_to_insert)

        if err_list:
            fill_in_err_table(['колонка','строка','значение'], err_list)
            global_vars.ui.err_tableWidget.setVisible(True) 
            global_vars.ui.footer_label.setStyleSheet('color: red')             
            global_vars.ui.footer_label.setText(f"Некоторые значения столбцов {global_vars.sample_columns} содержат некорректные значения")
        else:
            global_vars.ui.footer_label.setStyleSheet('color: green')             
            global_vars.ui.footer_label.setText(f"Столбцы {global_vars.sample_columns} содержат корректные значения")


    def starter(self):
        print('starter')
        self.start()   # Запускаем поток  



    def on_started(self): # Вызывается при запуске потока
        print('on_started')
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)        
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)
        global_vars.ui.pushButtonLoader.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False)         
        global_vars.ui.err_tableWidget.setVisible(False)  
        global_vars.ui.pushButtonLoader.setEnabled(True)                           


    
    def on_finished(self): # Вызывается при завершении потока
        print('on finished')
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(True)        
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(True)
        global_vars.ui.comboSheets.setEnabled(True)         
