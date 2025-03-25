from PySide6 import QtCore
import global_vars
from my_functions.main_window import fill_in_table, load_file_sheet_name
#from functions import load_file_sheet_name
# from colorama import Fore


class HeaderUpThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        load_file_sheet_name()

    def starter(self):
        global_vars.sheet_name = global_vars.ui.comboSheets.currentText()

        self.start()

    def on_started(self):
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)
        global_vars.ui.pushButtonLoader.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False)
        global_vars.ui.err_tableWidget.setVisible(False)

    def on_finished(self):
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(True)
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(True)
        if global_vars.file[-4:] in ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']:
            global_vars.ui.comboSheets.setEnabled(True)
            global_vars.ui.comboSheets.setVisible(True)

        if global_vars.header_row < len(global_vars.df):
            global_vars.header_row += 1
            global_vars.ui.footer_label.setStyleSheet('color: green')
            global_vars.ui.footer_label.setText(f'Заголовки подняты! Заголовки в строке {global_vars.header_row}')
        else:
            global_vars.ui.footer_label.setStyleSheet('color: red')
            global_vars.ui.footer_label.setText(f"Достигнут конец листа! Заголовки в строке "
                                                f"{global_vars.header_row}. Таблица не содержит данных!")
        fill_in_table()
