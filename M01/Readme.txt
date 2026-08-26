Access Control Demo
by Jennifer Bowers 8/26/2026

A Demo of Role-Based Access Control (RBAC) and Authentication for the SDEV245 M01 Assignment created in Python.
This application demonstrates how to implement the CIA Triad principles of Confidentiality by restricting access to certain features based on user roles, the principle of Integrity by ensuring that only authorized users can modify data (the Faux buttons), and the principle of Availability by providing access to authorized users while preventing unauthorized access.

Features
This application features a login screen (main window) and two user role screens: admin and user.
The admin and user windows have faux buttons to demonstrate the differences in accessibility
There is a manual login as well as instant access demo buttons, one for admin and another for user

Demo Usernames and Passwords:
    Admin: Username: admin, Password: Admin123
    User: Username: user, Password: User123

Prerequisites and installation
This application uses the built-in tkinter Python library.

Application Logic
This application starts with a main login window that allows manual input to log in or the use of two demo buttons: an admin and a user.
The login checks for correct credentials before allowing access to the assigned user role window.

If using the admin login options, it will pull up a screen for basic admin use that includes a welcome message that clearly states it is the admin page, as well as some nonworking buttons to simulate administrative uses. The faux buttons will pop an error stating they are demo only and nonfunctioning

If using the “user” login options, it will pull up a screen for basic user task buttons and include a welcome message that clearly states it is the user window.
The admin and user have different task buttons available to them. The buttons also are nonfunctioning and just for demonstrative purposes. The faux buttons will pop an error stating they are demo only and nonfunctioning

Should the login credentials fail, an error message will appear, clear the entry boxes, and refocus on the username entry box to allow another attempt.

All windows have a "quit" button that exits the application.
The admin and user windows also have a logout button that will return to the login screen.
The screens are gently color-coded to help the user notice quickly which authorization space they are accessing.
