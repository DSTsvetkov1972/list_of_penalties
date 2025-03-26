from PySide6 import QtWidgets
from my_windows import main_window
import global_vars
import config
from my_functions.main_window import header_down
# from colorama import Fore

from my_threads.log_in_check import LogInCheck
from my_threads.choose_file import ChooseFileThread
from my_threads.choose_sheet import ChooseSheetThread
from my_threads.open_file import OpenFileThread
from my_threads.preproc import PreprocThread
from my_threads.get_result import LoadInDWHThread
from my_threads.header_up import HeaderUpThread

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        global_vars.ui = main_window.Ui_MainWindow()
        global_vars.ui.setupUi(self)
        self.log_in_check_thread.start()

        global_vars.ui.action_log_in_check.triggered.connect(lambda: self.log_in_check_thread.start())

        global_vars.ui.action_show_manual.triggered.connect(self.show_manual)

        global_vars.ui.action_show_dev_info.triggered.connect(self.show_dev_info)

        global_vars.ui.pushButtonChooseFile.clicked.connect(self.choose_file_thread.starter)
        self.choose_file_thread.started.connect(self.choose_file_thread.on_started)
        self.choose_file_thread.finished.connect(self.on_finished_choose_file_thread)

        self.choose_sheet_thread.started.connect(self.choose_sheet_thread.on_started)
        self.choose_sheet_thread.finished.connect(self.choose_sheet_thread.on_finished)

        global_vars.ui.pushButtonUp.clicked.connect(self.header_up_thread.starter)
        self.header_up_thread.started.connect(self.header_up_thread.on_started)
        self.header_up_thread.finished.connect(self.header_up_thread.on_finished)

        global_vars.ui.pushButtonDown.clicked.connect(header_down)

        global_vars.ui.pushButtonOpenFile.clicked.connect(self.open_file_thread.starter)
        self.open_file_thread.started.connect(self.open_file_thread.on_started)
        self.open_file_thread.finished.connect(self.open_file_thread.on_finished)

        global_vars.ui.pushButtonPreprocessing.clicked.connect(self.preproc_thread.starter)
        self.preproc_thread.started.connect(self.preproc_thread.on_started)
        self.preproc_thread.finished.connect(self.preproc_thread.on_finished)

        global_vars.ui.pushButtonLoader.clicked.connect(self.load_in_dwh_thread_starter)
        self.load_in_dwh_thread.started.connect(self.load_in_dwh_thread.on_started)
        self.load_in_dwh_thread.finished.connect(self.load_in_dwh_thread.on_finished)

        global_vars.header_row = 1

    '''
    def show_log_in_dialog(self):
        self.login_dialog_window = LogInDialog(parent = None)
        # self.login_dialog_window.setWindowModality(True)
        self.login_dialog_window.show()
    '''

    def show_dev_info(self):
        QtWidgets.QMessageBox.about(None, "Контакты разработчиков", config.dev_info)

    def show_manual(self):
        QtWidgets.QMessageBox.about(None, "Инструкция", config.manual)

####################################################################################
####################################################################################

    log_in_check_thread = LogInCheck()         # создаём поток проверки подключения
    choose_file_thread = ChooseFileThread()    # создаём поток при загрузке файла
    choose_sheet_thread = ChooseSheetThread()  # создаём поток при загрузке листа
    header_up_thread = HeaderUpThread()        # создаём поток при поднятии заголовка
    open_file_thread = OpenFileThread()        # создаём поток при открытии файла
    preproc_thread = PreprocThread()           # создаём поток при проверке файла
    load_in_dwh_thread = LoadInDWHThread()     # создаём потоки загрузки файла

####################################################################################
####################################################################################

    def on_finished_choose_file_thread(self):
        # if global_vars.file[-4:] in config.file_formats_list:
        if global_vars.can_load_file:
            global_vars.ui.comboSheets.currentIndexChanged.connect(self.choose_sheet_thread.starter)
            global_vars.ui.comboSheets.clear()
            for sheet_name in global_vars.sheet_names:
                global_vars.ui.comboSheets.addItem(sheet_name)

            global_vars.ui.pushButtonUp.setEnabled(True)
            global_vars.ui.pushButtonDown.setEnabled(True)
            global_vars.ui.pushButtonOpenFile.setEnabled(True)
            global_vars.ui.header_label.setStyleSheet('color: black')
            global_vars.ui.header_label.setText(f'{global_vars.file}')
        else:
            global_vars.ui.header_label.setStyleSheet('color: red')
            global_vars.ui.header_label.setText('Выберите файл для загрузки')
            global_vars.ui.footer_label.setStyleSheet('color: red')
            global_vars.ui.footer_label.setText(f'Не удалось загрузить {global_vars.file} {global_vars.cant_load_file_reason}')

        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(True)

    def load_in_dwh_thread_starter(self):
        self.load_in_dwh_thread.start()  # Запускаем поток


################################################################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
