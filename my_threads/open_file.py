from PySide6 import QtCore
import global_vars
import os


class OpenFileThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        os.startfile(global_vars.file)

    def starter(self):
        self.start()

    def on_started(self):
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(False)
        global_vars.ui.verticalLayoutWidgetButtons_2.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False)
        # global_vars.ui.footer_text.setVisible(False)

    def on_finished(self):
        global_vars.ui.verticalLayoutWidgetButtons_1.setEnabled(True)
        global_vars.ui.footer_label.setStyleSheet('color: green')
        global_vars.ui.footer_label.setText(f"Файл {global_vars.file} открыт на рабочем столе.")
