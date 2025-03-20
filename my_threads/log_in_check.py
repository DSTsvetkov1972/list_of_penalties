from PySide6 import QtCore, QtWidgets
from colorama import Fore
# from my_functions.dwh import Client
from my_functions.main_window import translit, load_file_sheet_name
import global_vars
import pandas as pd
import re, os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import psycopg2 as ps
from psycopg2 import Error
import pickle
import os

class LogInCheck(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def create_keys_auth_request(self):
        # create a new RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # get the public key from the private key
        public_key = private_key.public_key()

        # the private key to PEM format
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # the public key to PEM format
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )


        # save the private key to files
        with open(os.path.join(os.getcwd(), 'private_key.pem'), 'wb') as f:
            f.write(private_key_pem)

        #with open('public_key.pem', 'wb') as f:
        #   f.write(public_key_pem)
        print("RSA keys have been generated successfully!")

        description = '''Параметры подключения к БД iSales' \
        для утилиты отдела таможеного оформления list_of_penalties' \
        пользователь Леутин А.С'''

        params = ['host','dbname','user','password','port']

        with open(os.path.join(os.getcwd(), 'auth_request'), 'wb') as fp:
            pickle.dump({'public_key':public_key_pem,
                        'description':description,
                        'params':params}, fp)    


    def get_params(self):
        """
        Получаем параметры подключения к БД iSales
        """
        try:
            with open(os.path.join(os.getcwd(),'auth_response'), 'rb') as file:
                encrypted = file.read()

            with open(os.path.join(os.getcwd(),"private_key.pem"), "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

            original_message = private_key.decrypt(
                encrypted,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return pickle.loads(original_message)
        except ValueError:
            return False

    

    def run(self):



        # если нет приватного ключа необходимого для получения доступа к БД, создаём его вместе с запросом на подключение
        if not os.path.exists(os.path.join(os.getcwd(),'private_key.pem')): 
            print(11111)
            self.create_keys_auth_request()
            if os.path.exists(os.path.join(os.getcwd(),'auth_response')):
                os.remove(os.path.join(os.getcwd(),'auth_response'))


            global_vars.ui.action_log_in_check.setEnabled(False)
            global_vars.ui.action_log_out.setEnabled(False)            
            global_vars.ui.login_label.setStyleSheet("color: red")
            global_vars.ui.login_label.setText("Получите файл аутентификации. Для этого отправьте файл auth_request сотрудинку, отвечающему за предоставление доступа!")
            global_vars.log_in_status = False
            return 
        elif not os.path.exists(os.path.join(os.getcwd(),'auth_response')):
            global_vars.ui.action_log_in_check.setEnabled(False)
            global_vars.ui.action_log_out.setEnabled(False)            
            global_vars.ui.login_label.setStyleSheet("color: red")
            global_vars.ui.login_label.setText("Поместите файл auth_response, полученный от сотрудинка, отвечающего за предоставление доступа в одну папку с файлом list_of_penalties.exe!")
            global_vars.log_in_status = False
            return 
        elif params := self.get_params():
            print(params)
            global_vars.ui.action_log_in_check.setEnabled(False)
            global_vars.ui.action_log_out.setEnabled(False)            
            global_vars.ui.login_label.setStyleSheet("color: red")            
            global_vars.ui.login_label.setText('Не удаётся подключиться с данным файлом auth_respons! Удалите файл private_key.pem из папки проекта и перезапустите программу, чтобы сформировать новый запрос на подключение') 
            global_vars.log_in_status = False
            return 
        else:
            global_vars.ui.login_label.setStyleSheet("color: blue")
            global_vars.ui.login_label.setText(f"Проверяем подключение к информационным ресурсам...")
           # try:
            print(params)
            with ps.connect(**params) as conn:
                cursor = conn.cursor()
                if conn.get_dsn_parameters():
                    global_vars.ui.login_label.setStyleSheet("color: green")
                    global_vars.ui.login_label.setText(f"Подключение к информационным ресурсам установлено!") 
                    global_vars.ui.action_log_in_check.setEnabled(True)
                    global_vars.ui.action_log_out.setEnabled(True) 
                    global_vars.log_in_status = True                
                    return  
            #except:
            #    global_vars.ui.login_label.setStyleSheet("color: red")
            #    global_vars.ui.login_label.setText(f"Не получается подключиться к информационным ресурсам!")                              
            #    global_vars.log_in_status = False

         



    def starter(self):
        pass

    def on_started(self): # Вызывается при запуске потока
        pass

    def on_finished(self): # Вызывается при завершении потока
        pass
