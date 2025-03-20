from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import pickle
import os


def create_keys_auth_request():
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

   params = ['host','db','login','password']

   with open(os.path.join(os.getcwd(), 'auth_request'), 'wb') as fp:
      pickle.dump({'public_key':public_key_pem,
                  'description':description,
                  'params':params}, fp)
      
if __name__ == '__main__':
   create_keys_auth_request()
