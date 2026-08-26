# AccessDemo.py
# This script is to demostrate the use of RBAC and CIA Triad in a Python application.

# Module 1: Assignment - RBAC and Authentication Mini-App
# SDEV245 Fall 2026
# Jennifer Bowers
# 8/25/2026

import tkinter as tk
from tkinter import messagebox

class AccessDemoApp(tk.Tk):
    """
    Creates the main application window for the Access Control Demo
    Demo of Role-Based Access Control (RBAC) and Authentication
    Demo Usernames and Passwords:
        Admin: Username: admin, Password: Admin123
        User: Username: user, Password: User123
    This application demonstrates how to implement CIA Triad principle of Confidentiality by restricting access to certain features based on user roles, principle of Integrity by ensuring that only authorized users can modify data (the Faux buttons), and principle of Availability by providing access to authorized users while preventing unauthorized access.

    """
    def __init__(self):
        super().__init__()

        self.title("Access Control Demo")
        self.geometry("400x300")

        # Initialize the current frame to None
        self.current_frame = None

        # Launch into inital screen
        self.switch_frame(Login)

    def switch_frame(self, frame_class, *args, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()
        # Instantiate the new frame and set it as the current frame
        self.current_frame = frame_class(self, *args, **kwargs)
        # Make the new frame fill the window
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

class Login(tk.Frame):
    """
    Creates the Login window for the Access Control Demo

    Parent window: Main Window

    """
    def __init__(self, parent):
        super().__init__(parent, bd = 4, relief = "groove")
        self.parent = parent
        self.configure(bg="lightblue")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Create the login widgets
        self.txt_login = tk.Label(self, text="Welcome to the Login Screen")
        self.txt_username = tk.Label(self, text="Username:")
        self.entry_username = tk.Entry(self)
        self.txt_password = tk.Label(self, text="Password:")
        self.entry_password = tk.Entry(self, show="*")
        self.btn_login = tk.Button(self, text="Login", command=self.login) # Validates the login credentials
        self.btn_quit = tk.Button(self, text="Quit", command=self.quit) # Closes the application

        # Demo button to show admin access
        self.btn_demo_admin = tk.Button(self, text="Demo Admin", command=lambda: self.parent.switch_frame(Admin, "Demo Admin"))
         # Demo button to show user access
        self.btn_demo_user = tk.Button(self, text="Demo User", command=lambda: self.parent.switch_frame(User, "Demo User")) 

        # Anchor the widgets to the grid layout
        self.txt_login.grid(row=0, column=0, columnspan = 2, sticky="ew", pady=20)
        self.txt_username.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_username.grid(row=1, column=1, sticky = "w", padx=10, pady=5)
        self.txt_password.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_password.grid(row=2, column=1, sticky = "w", padx=10, pady=5)
        self.btn_login.grid(row=3, column=1, columnspan=2, pady=10)
        self.btn_quit.grid(row=3, column=0, columnspan=2, pady=10)
        self.btn_demo_admin.grid(row=4, column=0, padx=5, pady=10)
        self.btn_demo_user.grid(row=4, column=1, padx=5, pady=10)

    def login(self):
        """
        Validates the login credentials and switches to the appropriate window based on access level.

        """
        # Gather the entry box contents
        username = self.entry_username.get()
        password = self.entry_password.get()
        username = username.lower()

        # Test if the login information is valid
        if username == "admin" and password == "Admin123":
            # Change the window to show only the admin access
            self.parent.switch_frame(Admin, username)
 
        elif username == "user" and password == "User123":
            # Change the window to show only the user access
            self.parent.switch_frame(User, username)
        else:
            # Display an error message for invalid login credentials
            messagebox.showerror("Login Failed", "Invalid username or password")
            # Clear the entry boxes and set focus back to the username entry
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

class Admin(tk.Frame):
    """
    Creates the Admin window for the Access Control Demo
    Parent window: Main Window
    Admin access is granted to the user with the username "admin" and password "Admin123"
    Admin access allows the user to manage work orders, incidents, and shifts.

    """
    def __init__(self, parent, username):
        super().__init__(parent, bd = 4, relief = "groove")
        self.parent = parent

        self.username = username.capitalize()
        self.configure(bg="lightseagreen")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.grid_anchor("center")

        # Create the admin widgets
        self.txt_admin = tk.Label(self, text="Admin Access Granted")
        self.txt_welcome = tk.Label(self, text=f"Welcome, {self.username}, to the Admin Window!")
        self.btn_logout = tk.Button(self, text="Logout", command=self.logout) # Returns to the login screen
        self.btn_quit = tk.Button(self, text="Quit", command=self.quit) # Closes the application
        self.btn_workorders_mgt = tk.Button(self, text="Work Orders Mgt", command = lambda: self.demo_only()) # Faux bottom for the work orders window
        self.btn_incident = tk.Button(self, text="Incident Mgt", command = lambda: self.demo_only() ) # Faux button for the incident management window
        self.btn_shift_management = tk.Button(self, text="Shift Mgt", command = lambda: self.demo_only() ) # Faux button for the shift management window

        # Anchor the widgets to the grid layout
        self.txt_admin.grid(row=0, column=0, columnspan = 3, sticky="nsew", pady=20, padx=5)
        self.txt_welcome.grid(row=1, column=0, columnspan=3, pady=10, padx=5)
        self.btn_workorders_mgt.grid(row=2, column=0, pady=10, padx=5)
        self.btn_incident.grid(row=2, column=1, pady=10, padx=5)
        self.btn_shift_management.grid(row=2, column=2, pady=10, padx=5)

        self.btn_logout.grid(row=3, column=0, columnspan=3, pady=10)
        self.btn_quit.grid(row=4, column=0, columnspan=3, pady=10)

    def logout(self):
        """
        Logs the user out and switches back to the login frame.
        """
        # Destroy the current frame and switch back to the login frame
        self.destroy()
        self.parent.switch_frame(Login)

        
    def demo_only(self):
        """
        Displays a message indicating that the button is a demo and does not perform any real functions.
        """
        messagebox.showerror("Demo Only", "This is a demo of admin task buttons. The buttons do not perform any real functions.")

class User(tk.Frame):
    """
    Creates the User window for the Access Control Demo
    Parent window: Main Window
    User access is granted to the user with the username "user" and password "User123"
    User access allows the user to view work orders, incidents, and shifts.

    """
    def __init__(self, parent, username):
        super().__init__(parent, bd = 4, relief = "groove")
        # Store the parent window and username for later use
        self.parent = parent
        self.username = username.capitalize()
        # Configure the frame's background color and grid layout
        self.configure(bg="lightgoldenrod")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.grid_anchor("center")

        # Create the user widgets
        self.txt_user = tk.Label(self, text="User Access Granted")
        self.txt_welcome = tk.Label(self, text=f"Welcome, {self.username}, to the User Window!")
        self.btn_logout = tk.Button(self, text="Logout", command=self.logout) # Returns to the login screen
        self.btn_quit = tk.Button(self, text="Quit", command=self.quit) # Closes the application
        self.btn_tasks = tk.Button(self, text="Tasks", command=lambda: self.demo_only()) # Faux button for the tasks window
        self.btn_tutorials = tk.Button(self, text="Tutorials", command=lambda: self.demo_only()) # Faux button for the tutorials window
        self.btn_workhours = tk.Button(self, text="Work Hours", command=lambda: self.demo_only()) # Faux button for the work hours window

        # Anchor the widgets to the grid layout
        self.txt_user.grid(row=0, column=0, columnspan = 3, sticky="nsew", pady=20, padx=5)
        self.txt_welcome.grid(row=1, column=0, columnspan = 3, pady=10, padx=5)
        self.btn_tasks.grid(row=2, column=0, sticky="ew", pady=10, padx=5)
        self.btn_tutorials.grid(row=2, column=1, sticky="ew", pady=10, padx=5)
        self.btn_workhours.grid(row=2, column=2, sticky="ew", pady=10, padx=5)
        self.btn_logout.grid(row=3, column=0, columnspan=4, pady=10)
        self.btn_quit.grid(row=4, column=0, columnspan=4, pady=10)

    def logout(self):
        """
        Logs the user out and switches back to the login frame.
        """
        # Destroy the current frame and switch back to the login frame
        self.destroy()
        self.parent.switch_frame(Login)

    def demo_only(self):
        """
        Displays a message indicating that the button is a demo and does not perform any real functions.
        """
        messagebox.showerror("Demo Only", "This is a demo of admin task buttons. The buttons do not perform any real functions.")


# Run the application
if __name__ == "__main__":
    app = AccessDemoApp()
    app.mainloop()