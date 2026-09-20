Secure Mock Email Client
Jennifer Bowers
9/14/2026

This mock email application was created to simulate CIA triad, encryption/decryption, and general security measures. It uses Python, Tkinter, SQLite3, and Cryptography library. The application uses a single window with secure, stack-based frame switching interfaces

Core CIA Triad Security Features

1. Robust Password Hashing and symmetric keys (bcrypt and PBKDF2HMAC)
    This application uses bcrypt for hashing and salting passwords before storing in the database. The result is stored as a blob. It also uses Password-Based Key Derivation Function (PBKDF2) to hash a password several thousand times and creating a user-unique key for encryption/decryption of emails

2. Symmetric Body Encryption (Fernet)
    Emails are encrypted before being stored as an unreadable blob in the database using user unique symmetric keys. The keys are generated uses cryptography.fernet and stored as bytes at user registration.

3. Role-Based Access Control (RBAC)
    Role are implemented into the system, assignable at registration for each user as "Student", "Professor", or "Administrator". Roles aside, the email application is strictly a single user interface. The goal was to add the ability to unlock emails by role for mass messages but for this assignment's scope it made more sense to lock by user instead of role.

4. On-The-Fly UI Isolation and Zero-Memory Leakage
    Usage isolation is implemented with all entry boxes being cleared when switching users so no data bleeding is present between users.

Requirements & Installation
    The following libraries need to be installed before running the application
    bcrypt cryptography (pip install bcrpyt)
    cryptography (pip install cryptography)


Application Usage

1. Register a user or log in to one of the mock users.
    On startup, if the database doesn't exist or is empty, a new one will be created and populated with the following users:
    alice_admin,  AdminPass@2026
    prof_smith,  SmithRule#101
    bob_student, BobPass!99
    If registering a new user, test out the password strength and integrity checks for both a matching password and unique username
2. Send an Email:
    Log in as a user.
    Head into the "Compose Email" tab,
    open the Recipient selection dropdown menu,
    select a user from the list,
    input an explicit message subject/body,
    and press "Encrypt & Send".
3. Inspect the Local Database:
    Open the generated file email_app.db using a SQLite Browser plugin or utility.
    Observe the emails table.
    The message subject will be readable for directory mapping, but the message body is stored as absolute unreadable binary BLOB string text.
4. Verify Secure Isolation:
    Log out of a user and log in as another user.
    Observe that the main Dashboard text frames are perfectly blank.
    Locate the incoming subject header inside your "Inbox View",
    click it and verify that the data automatically decrypts to print out the message text clearly inside your dashboard container.
5. Test against tampering of an email.
    To simulate an attack and tampering of an email:
    After loading up the SecureEmail.py application just once (to populate the database with sample users and emails),
    First read the emails for bob_student. Then run the application tamper_db.py
    Log into bob_student again. One of the emails should flag as being tampered with.