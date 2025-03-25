# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,Qt,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,QLineEdit, QComboBox,  QInputDialog,  
    QTableView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout,)
import config

from datetime import datetime



class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        #MainWindow.setFixedWidth(1366) 
        #MainWindow.setFixedHeight(768) 
        MainWindow.resize(1366, 724)
        MainWindow.setMaximumSize(1366, 724) 
        MainWindow.setMinimumSize(340, 724)         
        MainWindow.setWindowTitle(f"{config.prog_name} (ver.{config.version})")
        #MainWindow.setWindowTitle(f"Загрузка Excel или CSV в DWH (ver. {datetime.now().strftime('%Y-%m-%d %H:%M')})")        
       

        self.centralwidget = QWidget(MainWindow)

        self.verticalLayoutWidgetButtons_1 = QWidget(self.centralwidget)
        self.verticalLayoutWidgetButtons_1.setGeometry(QRect(10, 60, 320, 30))
        # self.verticalLayoutWidgetButtons_1.setStyleSheet("background-color: pink")
        self.verticalLayoutButtons_1 = QVBoxLayout(self.verticalLayoutWidgetButtons_1)
        self.verticalLayoutButtons_1.setContentsMargins(10, 0, 0, 0) 

        self.verticalLayoutWidgetButtons_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidgetButtons_2.setGeometry(QRect(10, 90, 320, 150))
        # self.verticalLayoutWidgetButtons_2.setStyleSheet("background-color: yellow")  
        self.verticalLayoutButtons_2 = QVBoxLayout(self.verticalLayoutWidgetButtons_2)
        self.verticalLayoutButtons_2.setContentsMargins(10, 0, 0, 0)    

        self.pushButtonChooseFile = QPushButton('Выбрать файл')
        self.pushButtonChooseFile.setEnabled(False)
        self.verticalLayoutButtons_1.addWidget(self.pushButtonChooseFile)

        self.pushButtonUp = QPushButton("Поднять заголовок")
        self.pushButtonUp.setEnabled(False)
        self.verticalLayoutButtons_2.addWidget(self.pushButtonUp)

        self.pushButtonDown = QPushButton("Опустить заголовок")
        self.pushButtonDown.setEnabled(False)        
        self.verticalLayoutButtons_2.addWidget(self.pushButtonDown)

        self.pushButtonOpenFile = QPushButton("Открыть на рабочем столе")
        self.pushButtonOpenFile.setEnabled(False)        
        self.verticalLayoutButtons_2.addWidget(self.pushButtonOpenFile)

        self.pushButtonPreprocessing = QPushButton("Проверить контейнеры и подкоды перовозок")
        self.pushButtonPreprocessing.setEnabled(False)        
        self.verticalLayoutButtons_2.addWidget(self.pushButtonPreprocessing)

        self.pushButtonLoader = QPushButton("Сформировать отчет")
        self.pushButtonLoader.setEnabled(False)        
        self.verticalLayoutButtons_2.addWidget(self.pushButtonLoader)



        self.verticalLayoutInfoWidget = QWidget(self.centralwidget)
        self.verticalLayoutInfoWidget.setGeometry(QRect(10, 240, 330, 404))
        #self.verticalLayoutInfoWidget.setStyleSheet("background-color: pink")
        self.verticalLayoutInfo= QVBoxLayout(self.verticalLayoutInfoWidget)
        #self.verticalLayoutInfo.setContentsMargins(10, 10, 10, 10)    
      
        self.err_tableWidget = QTableWidget()
        self.verticalLayoutInfo.addWidget(self.err_tableWidget)
        self.err_tableWidget.setVisible(False)
        
        #self.pushButton_4 = QPushButton("Кнопочка")
        #self.verticalLayoutInfo.addWidget(self.pushButton_4)


        self.verticalLayoutWidgetRight = QWidget(self.centralwidget)
        self.verticalLayoutWidgetRight.setGeometry(QRect(340, 60, 1000, 598))
        self.verticalLayoutRight = QVBoxLayout(self.verticalLayoutWidgetRight)
        self.verticalLayoutRight.setContentsMargins(10, 0, 0, 0)
        
        self.login_label = QLabel('Подключитесь к DWH!')
        self.login_label.setStyleSheet('color: red')
        self.verticalLayoutRight.addWidget(self.login_label)

        self.header_label = QLabel('Выберите файл для загрузки!')
        self.header_label.setStyleSheet('color: red')
        self.verticalLayoutRight.addWidget(self.header_label)

        self.comboSheets = QComboBox()
        self.comboSheets.setFixedWidth(200)        
        self.comboSheets.setVisible(False)  
        self.verticalLayoutRight.addWidget(self.comboSheets)

        self.tableWidget = QTableWidget()
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalLayoutRight.addWidget(self.tableWidget)

        self.footer_label = QLabel()
        self.verticalLayoutRight.addWidget(self.footer_label)

        self.footer_text = QLineEdit()
        self.footer_text.setReadOnly(True) 
        self.footer_text.setVisible(False)
        self.verticalLayoutRight.addWidget(self.footer_text)

#####################################################################################
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1366, 28))
      
        #self.menu = QMenu(self.menubar)
        #self.menu.setTitle("Подключение к DWH")
        #self.menubar.addAction(self.menu.menuAction())           

        #self.action_log_in = QAction(MainWindow)
        #self.action_log_in.setText("Подключиться")  
        #self.menu.addAction(self.action_log_in)

        self.action_log_in_check = QAction(self.menubar)
        self.action_log_in_check.setText("Проверить подключение")
        self.action_log_in_check.setEnabled(True)        
        self.menubar.addAction(self.action_log_in_check)         

        
        #self.action_log_out = QAction(MainWindow)
        #self.action_log_out.setText("Отключиться")
        #self.menu.addAction(self.action_log_out)  
       

        self.action_show_manual = QAction(self.menubar)
        self.action_show_manual.setText("Инструкция") 
        self.menubar.addAction(self.action_show_manual)  

        self.action_show_dev_info = QAction(self.menubar)
        self.action_show_dev_info.setText("Связь с разработчиками") 
        self.menubar.addAction(self.action_show_dev_info)           
        
