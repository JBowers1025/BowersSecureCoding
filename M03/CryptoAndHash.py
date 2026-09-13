# CryptoAndHash.py
# Cryptography Demostration Tool
# Jennifer Bowers
# 9/10/2026

# This App is a demostration of salting, hashing, encrypting and decrypting simple messages with Caesar Ciphers

import os
os.system ('cls')
import sys
import hashlib
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

def generate_SHA256(text):
    '''Generates SHA256 hashing from a string'''
    # Strings must be encoded to bytes first
    input = text.encode('utf-8')
    hashed_text = hashlib.sha256(input)
    return hashed_text.hexdigest()

def caesar_cipher(text, shift, decrypt=False):
    """Encrypts or decrypts text shifting letters by a fixed amount."""
    if decrypt:
        shift = -shift
    
    result = ""
    for char in text:
        # Process uppercase characters
        if char.isupper():
            # (Current Position + Shift - Start Position) % AlphabetSize + Start Position
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Process lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        # Leave spaces, numbers, and punctuation exactly as they are
        else:
            result += char
    return result


def run_signature_demo():
    """Demostrates OpenSSL Digital Signing """

    print ("\n Generating OpenSSL RSA Keys \n")
    # Generate keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    print("Key creation successful and saved")

    # Signature message
    signature_message = b"Authentic Message 123"
    print(f"Signing Message: '{signature_message.decode()}")

    # This generates raw bytes signature
    signature = private_key.sign(
        signature_message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    # Convert to readable text
    display_sig = base64.b64encode(signature).decode('utf-8')
    print(f"Generated Signature: \n {display_sig[:60]} ...")

    print('\n Verify Signature')
    try:
        public_key.verify(
            signature,
            signature_message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("Verfication process successful: Message is authentic")
    except InvalidSignature:
        print("Verfication Failed, message may have been tampered with.")

    print("\n Simulating Tampering Attack")
    tampered_message = b"Authentic Message 456"
    print(f"Attacker changed the message to: '{tampered_message}'")
    try:
        public_key.verify(
            signature,
            tampered_message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("Verfication process successful: Message is authentic")
    except InvalidSignature:
        print("Alarm Triggers: Signature failed verfication process. Data has been tampered with.")

def CryptoHashMain():
    """ Central processing for the demostration """
    while True:
        print("\nCryptography Demostration \n" \
        "Presenting Caesar Cipher, SHA256, OpenSSL Digital Signatures \n" \
        "\n" \
        "1. Generate SHA-256 Hash \n" \
        "2. Encrypt Caesar Cipher Message \n" \
        "3. Decrypt Caesar Cipher Message \n" \
        "4. Simulate Digital Signature (OpenSSL)\n" \
        "5. Exit")

        choice = input ("\n Choose an option (1-5):").strip()

        if choice == '1':
            text = input("Enter a message to hash: \n")
            print(f"\nSHA-256 Hash: \n {generate_SHA256(text)}\n")

        elif choice == "2":
            text = input("Enter a message to encrypt: \n")
            shift = int(input("Enter the value for the shift (example: 7): "))
            print(f"\nEncrypted Text: {caesar_cipher(text, shift)}\n")

        elif choice == "3":
            text = input("Enter a text to decrypt: \n")
            shift = int(input("Enter the value for the shift (example: 7): "))
            print(f"\nDecrypted Message: {caesar_cipher(text, shift, decrypt= True)}\n")

        elif choice == "4":
            run_signature_demo()

        elif choice == "5":
            print("Thanks for running this program, Goodbye!")
            sys.exit()

        else:
            print("Invalid option, please choose 1-5.")
            

if __name__ == "__main__":
   CryptoHashMain()            