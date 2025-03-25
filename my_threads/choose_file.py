from PySide6 import QtWidgets, QtCore
# from colorama import Fore
import global_vars
import config
import pandas as pd
import os


class ChooseFileThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        if not global_vars.file:
            global_vars.ui.header_label.setStyleSheet('color: red')
            global_vars.ui.header_label.setText('Выберите файл для загрузки')
            global_vars.ui.footer_label.setStyleSheet('color: red')
            global_vars.cant_load_file_reason = 'Вы не выбрали файл!'
            global_vars.can_load_file = False
            return

        if os.path.getsize(global_vars.file) == 0:
            global_vars.ui.header_label.setStyleSheet('color: red')
            global_vars.ui.header_label.setText('Выберите файл для загрузки')
            global_vars.ui.footer_label.setStyleSheet('color: red')
            global_vars.cant_load_file_reason = 'Пустой файл не может быть загружен!'
            global_vars.can_load_file = False
        else:
            if global_vars.file[-4:] in config.file_formats_list:
                try:
                    with pd.ExcelFile(global_vars.file) as excel_file_obj:
                        global_vars.sheet_names = excel_file_obj.sheet_names
                    global_vars.can_load_file = True
                except ValueError:
                    global_vars.cant_load_file_reason = 'Файл не читается обработчиком эксель-файлов!'
                    global_vars.can_load_file = False
            else:
                global_vars.df = pd.DataFrame()
                global_vars.cant_load_file_reason = f'Файл должен быть в формате: {config.file_formats_list}!'
                global_vars.can_load_file = False

    def starter(self):
        global_vars.ui.comboSheets.setVisible(False)
        global_vars.header_row = 0
        global_vars.ui.tableWidget.setRowCount(0)
        global_vars.ui.tableWidget.setColumnCount(0)
        global_vars.ui.tableWidget.clear()
        global_vars.file = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.start()

    def on_started(self):
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False)
        global_vars.ui.err_tableWidget.clear()
        global_vars.ui.err_tableWidget.setVisible(False)
        global_vars.ui.header_label.setText('')
        global_vars.ui.footer_label.setStyleSheet('color: blue')
        global_vars.ui.footer_label.setText(f"Загружаем для предпросмотра "
                                            f"{global_vars.file}...")
