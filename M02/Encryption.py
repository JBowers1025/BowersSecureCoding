# Encryption.py
# Jennifer Bowers
# 9/1/2026

# This program encrypts a message, demostrating asymmetric and symmetric encryption methods.
# Installing the library module "rsa" and "cryptography" is required to run this program.

import os
os.system("cls") # Clears the ouput (terminal) screen at beginng of the program.

import rsa # Import the rsa module for asymmetric encryption
from cryptography.fernet import Fernet # Import the Fernet class from the cryptography module for symmetric encryption

class Asymmetric:
    '''Class to handle encryption and decryption of messages using RSA asymmetric encryption.'''
    def __init__(self, message):
        self.message = message
        self.public_key, self.private_key = self.create_keys()

    def create_keys(self):
        # Generate a new public/private key pair
        key_size = 1024  # Key size in bytes (1024 bits)
        public_key, private_key = rsa.newkeys(key_size)
        return public_key, private_key
        
    def encrypt(self):
        # Encrypt the message using the public key
        encrypted_message = rsa.encrypt(self.message.encode(), self.public_key)
        print("\n Message is now encrypted using asymmetric encryption: \n", encrypted_message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        # Decrypt the message using the private key
        decrypted_message = rsa.decrypt(encrypted_message, self.private_key).decode()
        print("\n Keys used for asymmetric encryption:")
        print("Public Key:", self.public_key)
        print("Private Key:", self.private_key)
        print("\n Decrypted message: \n", decrypted_message)
        return decrypted_message

class Symmetric:
    '''Class to handle encryption and decryption of messages using symmetric encryption via the Fernet class from the cryptography module.'''
    def __init__(self, message):
        self.message = message

    def encrypt(self):
        self.key = Fernet.generate_key() # Generate a symmetric key for encryption
        self.cipher_suite = Fernet(self.key) # Create a Fernet cipher suite using the generated key

        # Encrypt the message using the symmetric key
        encrypted_message = self.cipher_suite.encrypt(self.message.encode())
        print("\n Message is now encrypted using symmetric encryption: \n", encrypted_message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        # Decrypt the message using the symmetric key
        decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
        print("\n Keys used for symmetric encryption: \n", self.key)
        print("\n Decrypted message: \n", decrypted_message)
        return decrypted_message

# Set variable new_msg to "yes" to start the loop for encrypting messages. The loop will continue until the user chooses not to encrypt another message.
new_msg = "yes"

while new_msg.lower() == "yes":
    # Prompt the user to choose the type of encryption
    Encryption_type = input("\n Enter '1' for asymmetric encryption or '2' for symmetric encryption: ")

    if Encryption_type == '1':
        # Prompt the user to enter a message for asymmetric encryption
        message = input("\n Enter the message you want to encrypt asymmetrically, long messages take longer to encrypt: \n")
        encrypt_type = Asymmetric(message)
        encrypted = encrypt_type.encrypt()

        # If the user chooses to decrypt, call the decryption function and display the decrypted message
        decrypted = input("\n Do you want to decrypt the message? (yes/no): ")

        if decrypted.lower() == 'yes':
            encrypt_type.decrypt(encrypted)
        else:
            print("\n Decryption skipped.")

        # Prompt the user to encrypt another message
        new_msg = input("\n Do you want to encrypt another message? (yes/no): ")

    elif Encryption_type == '2':
        # Prompt the user to enter a message for symmetric encryption
        message = input("\n Enter the message you want to encrypt symmetrically: \n")
        encrypt_type = Symmetric(message)
        encrypted = encrypt_type.encrypt()

        # If the user chooses to decrypt, call the decryption function and display the decrypted message
        decrypted = input("\n Do you want to decrypt the message? (yes/no): ")

        if decrypted.lower() == 'yes':
            encrypt_type.decrypt(encrypted)
        else:
            # Decryption is skipped
            print("\n Decryption skipped.")

        # Prompt the user to encrypt another message
        new_msg = input("\n Do you want to encrypt another message? (yes/no): ")
        

    else:
        # Handle invalid input
        print("Invalid input. Please enter '1' or '2'.")
        new_msg = input("\n Do you want to try again? (yes/no):")
        


