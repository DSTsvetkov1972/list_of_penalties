from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import pickle
import os


def get_params():
    """
    Получаем параметры подключения к БД iSales
    """
    try:
        with open(os.path.join(os.getcwd(),'auth_response'), 'rb') as file:
            encrypted = file.read()
    except FileNotFoundError as e:
        return e

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

if __name__ == '__main__':
    print(get_params())