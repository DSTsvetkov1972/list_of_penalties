from PySide6 import QtWidgets, QtCore
from pandas import DataFrame
from colorama import Fore 
import global_vars
from time import sleep


class MyComboBoxFormats(QtWidgets.QComboBox):
    def __init__(self, column_name, column_number):
        super().__init__()
        self.addItem("String")                    
        self.addItem("Date")
        self.addItem("DateOrNull")            
        self.addItem("DateTime")
        self.addItem("DateTimeOrNull")            
        self.addItem("Int32")
        self.addItem("Int32OrNull")                  
        self.addItem("Float32") 
        self.addItem("Float32OrNaN")  
        self.addItem("Container")        
        self.addItem("Vagon")          
        #globals.ui = ui
        self.column_name = column_name
        self.column_number = column_number

        self.background_color = 'background-color: none'

        self.rows_to_check = 0
        self.checked_rows = 0
         
        self.err_df = self.no_errs_df = DataFrame(columns = ['column_number','Сообщение','Ячейка LN','Ячейка RNCN','Значение'])

        global_vars.ui.checks_result_df = self.no_errs_df 


    @classmethod
    def print_all(cls):
        for instance in cls.instances:
            try:
                print(Fore.YELLOW, f'***{instance.test}***' ,Fore.WHITE)
            except:
                print(Fore.RED, f'{instance} не имеет атрибута test', Fore.WHITE)


    @classmethod
    def set_eanbled_all(cls, flag):
        for instance in cls.instances:
            instance.setEnabled(flag)       


    @classmethod
    def on_cheks_finished(cls):
        for instance in cls.instances:
            instance.rows_to_check = 0
            instance.checked_rows = 0
            instance.setStyleSheet(instance.style_sheet)
            cls.err_df 
        cls.err_df = instance.err_df = DataFrame(columns = ['column_number','Сообщение','Ячейка LN','Ячейка RNCN','Значение'])
        cls.set_eanbled_all(True)       
    

    @classmethod
    def fill_in_err_table_cls(cls):
        global_vars.ui.err_tableWidget.setRowCount(len(cls.all_err_df))
        global_vars.ui.err_tableWidget.setColumnCount(4)  
        global_vars.ui.err_tableWidget.setHorizontalHeaderLabels(['Ошибка','Ячейка','Ячейка','Значение'])
        #ui.tableWidget.setVerticalHeaderLabels(self.verticalHeaders)
        
        # Заполнить вьюшку
        row_number = 0
        for row in cls.all_err_df.itertuples():
            column_number = 0
            for item in row[2:]:
                cellinfo = QtWidgets.QTableWidgetItem(str(item))
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                global_vars.ui.err_tableWidget.setItem(row_number, column_number, cellinfo)
                column_number += 1
            row_number +=1              


    def check_starter(self):
        self.check_starter_thread.start()      


    def on_started_check_starter_thread(self):
        sleep(0.1)
        #self.load_file_sheet_name()
        #self.setEnabled(False)
        self.setStyleSheet("background-color: yellow")
        
        global_vars.ui.tableWidget.setEnabled(False)  
              
        self.rows_to_check = len(global_vars.df)  

        global_vars.ui.err_tableWidget.clear()
        global_vars.ui.err_tableWidget.setVisible(False)
        global_vars.ui.footer_text.setVisible(False)

        #global_vars.ui.checks_started_qty += 1
        #global_vars.ui.footer_label.setStyleSheet('color: blue')
        #global_vars.ui.footer_label.setText(f"Запущено проверок {global_vars.ui.checks_started_qty}")


    def on_finished_check_starter_thread(self):
        print(f'Проверка вошли в on_finished {global_vars.check_result_style_sheet}')
        self.setStyleSheet(global_vars.check_result_style_sheet) 
        #global_vars.ui.checks_started_qty -= 1     
        #global_vars.ui.footer_label.setText(f"Запущено проверок {global_vars.ui.checks_started_qty}") 
        #self.setEnabled(True) 
        global_vars.ui.tableWidget.setEnabled(True)

    def on_signal(self,s):
        
        if s[0] == 'checks':
            signal_type, column_number, cells_to_check, cells_checked = s
            global_vars.checks_dict[column_number] = (cells_to_check, cells_checked)
            cells_to_check_total = 0
            cells_checked_total = 0
            for value in global_vars.checks_dict.values():
                cells_to_check_total += value[0]
                cells_checked_total += value[1]
                global_vars.my_signal_message = f'Проверено {cells_checked_total} ячеек из {cells_to_check_total}...'
                #global_vars.ui.footer_label.setText(f'Проверено {cells_checked_total} ячеек из {cells_to_check_total}...')
        elif s[0] == 'fill_in_err_table':
            signal_type, rows_ready, total_rows = s
            global_vars.my_signal_message = f'Подготавливаем к выводу список ошибок. Заполнено {rows_ready} строк из {total_rows}...'
            #global_vars.ui.footer_label.setText(f'Подготавливаем к выводу список ошибок. Заполнено {rows_ready} строк из {total_rows}...')    
        else:
            global_vars.my_signal_message = f'Принят загадочный сигнал...'
            #global_vars.ui.footer_label.setText(f'Принят загадочный сигнал...')  
        global_vars.ui.footer_label.setStyleSheet('color: blue')  
        global_vars.ui.footer_label.setText(global_vars.my_signal_message)  
