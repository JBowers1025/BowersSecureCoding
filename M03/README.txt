Cryptography Demostration Tool
CryptoAndHash.py

Jennifer Bowers
9/10/2026

This is a app for demostrating the understanding of hashing, caesar ciphers, and digital signatures verifying authenticity.

Dependencies
This project using several built in libraries but does require the installation of Cryptography

Install Cryptography by
pip install cryptography

Features and Functionalities

1) SHA-256 Hashing Tool
Function: Compresses the input string itno a unique and fixed 256bit hex signature.
Security Context: Demostrated the principal of data integrity and one way mathamatical Functions

2) Caesar Substitution ciphers (Encryption and Decryption)
Function: Implementing a symmetrical caesar cipher algorithm with a specificed shift value
Security Context: Demostrates data confidentialitiy concepts with a reversable encrypt/decryption with the same key

3) OpenSSL Digital Signature Simulation
Function: Generatges ad a 2048-bit RSA keypair, similuting public and private keys used for file authenticity signatures
Security Context: Demostrates real-world simulation of data integrity and flagging for tampering

How to run
Automactically with the edittor run function or in command terminal:
python CryptoAndHash.py