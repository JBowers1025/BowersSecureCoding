# SecureEmail.py
# Jennifer Bowers 9/14/2026
# M04 Midterm Assignment

# This application is to demonstrate the understanding of the CIA triad, encryption, hashing and digital signatures,
# in the form of a simple school email app.

import os
os.system('cls' if os.name == 'nt' else 'clear')
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import bcrypt
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import re

# ---------------------------------------
# 1. DATABASE & SECURITY SETUP
# ---------------------------------------
def init_db():
    """Initializes the database and pre-populates mock users and encrypted emails."""
    conn = sqlite3.connect("email_app.db")
    cursor = conn.cursor()

    # Create tables if they do not exist
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password_hash BLOB NOT NULL,
                   crypto_salt BLOB NOT NULL,
                   role TEXT NOT NULL
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS emails
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       sender TEXT NOT NULL,
                       recipient TEXT NOT NULL,
                       subject TEXT NOT NULL,
                       encrypted_body BLOB NOT NULL
                   )
                   """)
    conn.commit()

    # Check if the database is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("[*] Pre-populating empty database with mock users and encrypted data...")

        # Mock Users: (Username, PlaintextPassword, Role)
        mock_users = [
            ("alice_admin", "AdminPass@2026", "Administrator"),
            ("prof_smith", "SmithRules#101", "Professor"),
            ("bob_student", "BobPass!99", "Student")
        ]

        # Dictionary to store user cryptographic salts
        user_salts = {}


        for username, password, role in mock_users:
            hashed_auth = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            encryption_salt = os.urandom(16)
            user_salts[username] = encryption_salt

            cursor.execute(
                "INSERT INTO users (username, password_hash, crypto_salt, role) VALUES (?, ?, ?, ?)",
                (username, hashed_auth, encryption_salt, role)
            )
        conn.commit()

        # Create and Encrypt sample messages for each inbox
        sample_messages = [
            {
                "sender": "alice_admin",
                "recipient": "prof_smith",
                "subject": "System Upgrade Maintenance Notification",
                "body": "Hello Professor Smith, the campus grading server will undergo a security patch window this Friday at midnight."
            },
            {
                "sender": "prof_smith",
                "recipient": "bob_student",
                "subject": "Assignment Extension Request Status",
                "body": "Hi Bob, I have reviewed your documentation. Your extension request has been approved. Your new deadline is Monday morning."
            },
            {
                "sender": "alice_admin",
                "recipient": "bob_student",
                "subject": "Campus Network Notice",
                "body": "Welcome back to school, Bob! Remember to reset your active Wi-Fi credentials before the semester begins."
            }
        ]

        for email in sample_messages:
            recip = email["recipient"]
            salt = user_salts[recip]

            # Recreate the routing key passphrase
            mock_passphrase = f"{recip}_secured_passphrase"
            derived_key = derive_user_key(mock_passphrase, salt)
            cipher_suite = Fernet(derived_key)

            # Perform symmetric body encryption
            encrypted_payload = cipher_suite.encrypt(email["body"].encode('utf-8'))

            cursor.execute(
                "INSERT INTO emails (sender, recipient, subject, encrypted_body) VALUES (?, ?, ?, ?)",
                (email["sender"], recip, email["subject"], encrypted_payload)
            )
        conn.commit()
        print("[+] Mock database successfully preloaded.")

    conn.close()


def derive_user_key(password: str, salt: bytes) -> bytes:
    """Derives a deterministic 32-byte Fernet key from a password and salt using PBKDF2."""
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000, # Industry standard stretching rounds
    )
    # Fernet requires a URL-safe base64-encoded 32-byte key
    return base64.urlsafe_b64encode(key.derive(password.encode('utf-8')))


def register_user(username, password, role):
    """Registers unique users with encrypted passwords and roles """
    if not username or not password or not role:
        return "Please fill out all fields."

    # Checks for password strength
    if not validate_password_strength(password):
         return "Password must be at least 8 characters long, contain a capital letter, number, and a symbol."

    # Bcrypt handles password authentication hashing automatically
    hashed_auth_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Generate a fresh, random 16-byte salt specifically for data encryption key derivation
    encryption_salt = os.urandom(16)

    conn = sqlite3.connect("email_app.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, crypto_salt, role) VALUES (?, ?, ?, ?)",
            (username, hashed_auth_pass, encryption_salt, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()


def validate_password_strength(password: str) -> bool:
    """
    Validates that a password meets complexity rules:
    - Min 8 characters long
    - At least 1 capital letter (A-Z)
    - At least 1 number (0-9)
    - At least 1 special character/symbol
    """
    # Pattern explanation:
    # (?=.*[A-Z])       -> Looks ahead for at least one uppercase letter
    # (?=.*\d)          -> Looks ahead for at least one digit
    # (?=.*[\W_])       -> Looks ahead for at least one symbol
    # .{8,}             -> Matches a total length of 8 or more characters
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"

    if re.match(pattern, password):
        return True
    return False

def login_user(username, password):
    """Verifies credentials and returns the unique session key if valid."""
    conn = sqlite3.connect("email_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, crypto_salt, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
        stored_salt = row[1]
        role = row[2] if (len(row) > 2 and row[2] is not None) else "Student"
        # Match the deterministic user routing identity key used in compose stage
        recipient_mock_passphrase = f"{username}_secured_passphrase"
        user_session_key = derive_user_key(recipient_mock_passphrase, stored_salt)
        return user_session_key, role
    return None


# ---------------------------------------
# 2. MAIN APPLICATION
# ---------------------------------------

class EmailApp(tk.Tk):
    """Root portion to the email app"""
    def __init__(self):
        """Creates the main window"""
        super().__init__()
        self.title("Secure Mock Email Client")
        self.geometry("650x550")
        self.current_user = None
        self.current_user_key = None  # Holds the unique derived Fernet key in memory during session
        self.current_user_role = None

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        """Shows a frame for a given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# ---------------------------------------
# 3. INDIVIDUAL FRAMES
# ---------------------------------------

class LoginFrame(tk.Frame):
    """"Login frame"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title_lbl = tk.Label(self, text="Secure Email System Login", font=("Arial", 16, "bold"))
        self.title_lbl.pack(pady=40)

        self.user_lbl = tk.Label(self, text="Username:")
        self.user_lbl.pack(pady=2)
        self.user_entry = tk.Entry(self, width=30)
        self.user_entry.pack(pady=5)
        self.user_entry.delete(0, tk.END)

        self.pass_lbl = tk.Label(self, text="Password:")
        self.pass_lbl.pack(pady=2)
        self.pass_entry = tk.Entry(self, width=30, show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.delete(0, tk.END)

        self.attempt_login_btn = tk.Button(self, text="Log In", width=15, bg="#4CAF50", fg="white", command=self.attempt_login)
        self.attempt_login_btn.pack(pady=15)
        self.register_btn = tk.Button(self, text="Register / Sign Up", width=15, command= lambda: self.controller.show_frame("RegisterFrame"))
        self.register_btn.pack(pady=2)

    def on_show(self):
        """Clears the login text boxes at startup"""
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)


    def attempt_login(self):
        """Login function, verifying the credentials"""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()

        # Verify credentials and pull down encryption configurations along with user role
        login_result = login_user(username, password)
        if login_result:
            session_key, role = login_result
            self.controller.current_user = username
            self.controller.current_user_role = role
            self.controller.current_user_key = session_key
            self.controller.show_frame("DashboardFrame")
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Auth Error", "Invalid credentials provided.")


class RegisterFrame(tk.Frame):
    """Register frame to registering a new user."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title_lbl = tk.Label(self, text="Create New User Account", font=("Arial", 16, "bold"))
        self.title_lbl.pack(pady=20)

        self.user_lbl = tk.Label(self, text="Choose Username:")
        self.user_lbl.pack(pady=2)
        self.reg_user_entry = tk.Entry(self, width=30)
        self.reg_user_entry.pack(pady=5)

        self.pass_lbl = tk.Label(self, text="Choose Password:")
        self.pass_lbl.pack(pady=2)
        self.reg_pass_entry = tk.Entry(self, width=30, show="*")
        self.reg_pass_entry.pack(pady=5)

        # Bind key release to monitor live strength validation on the primary password field
        self.reg_pass_entry.bind("<KeyRelease>", self.evaluate_live_strength)

        # Confirm Password Input Field
        self.pass2_lbl = tk.Label(self, text="Confirm Password:")
        self.pass2_lbl.pack(pady=2)
        self.reg_confirm_pass_entry = tk.Entry(self, width=30, show="*")
        self.reg_confirm_pass_entry.pack(pady=5)

        # Live password strength status text label component
        self.strength_lbl = tk.Label(self, text="Strength: Empty", fg="grey", font=("Arial", 9, "bold"))
        self.strength_lbl.pack(pady=2)

        # Helper text displaying the password requirements
        self.helper_lbl = tk.Label(self, text="(Requires: Min 8 chars, 1 Capital, 1 Number, 1 Symbol)", font=("Arial", 8, "italic"),
                 fg="dimgrey")
        self.helper_lbl.pack(pady=2)

        self.role_lbl = tk.Label(self, text="Assign Application Role:")
        self.role_lbl.pack(pady=2)
        self.role_combo = ttk.Combobox(self, width=27, values=["Student", "Professor", "Administrator"],
                                       state="readonly")
        self.role_combo.set("Student")
        self.role_combo.pack(pady=5)

        self.attempt_login_btn = tk.Button(self, text="Register Account", width=18, bg="#008CBA", fg="white", command=self.attempt_signup)
        self.attempt_login_btn.pack(pady=15)
        self.login_btn = tk.Button(self, text="Back to Login", width=18, command=lambda: self.controller.show_frame("LoginFrame"))
        self.login_btn.pack(pady=2)

    def evaluate_live_strength(self, event):
        """Monitors typing states continuously to print active strength levels inside UI."""
        password = self.reg_pass_entry.get()
        if not password:
            self.strength_lbl.config(text="Strength: Empty", fg="grey")
            return

        if validate_password_strength(password):
            self.strength_lbl.config(text="Strength: Strong Password (Meets Requirements)", fg="green")
        else:
            self.strength_lbl.config(text="Strength: Weak Password (Missing Requirements)", fg="red")

    def on_show(self):
        """Resets the registration input form fields completely"""
        self.reg_user_entry.delete(0, tk.END)
        self.reg_pass_entry.delete(0, tk.END)
        self.reg_confirm_pass_entry.delete(0, tk.END)  # Clear confirm field
        self.strength_lbl.config(text="Strength: Empty", fg="grey")
        self.role_combo.set("Student")

    def attempt_signup(self):
        """Signup function, verifying the credentials"""
        username = self.reg_user_entry.get().strip()
        password = self.reg_pass_entry.get()
        confirm_password = self.reg_confirm_pass_entry.get()  # Fetch confirmation text
        role = self.role_combo.get()

        # 1. Check for complete empty parameters
        if not username or not password or not confirm_password or not role:
            messagebox.showerror("Registration Error", "Please fill out all fields.")
            return

        # 2. Confirm password mismatch guard logic check
        if password != confirm_password:
            messagebox.showerror("Security Error", "Passwords do not match. Please verify your entry.")
            return

        # 3. Validate pattern matching structure rules
        if not validate_password_strength(password):
            messagebox.showerror("Security Error", "Your password does not satisfy complexity standard policies.")
            return

        result = register_user(username, password, role)
        if result is True:
            messagebox.showinfo("Success", f"Account '{username}' ({role}) registered! Redirecting to login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Registration Error", f"{result}")

class DashboardFrame(tk.Frame):
    """Dashboard of the application, once user has logged in successfully"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.user_label = tk.Label(self, text="", fg="darkblue", font=("Arial", 10, "italic"))
        self.user_label.pack(anchor="w", padx=10, pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.inbox_tab = tk.Frame(self.notebook)
        self.compose_tab = tk.Frame(self.notebook)

        self.notebook.add(self.inbox_tab, text="Inbox View")
        self.notebook.add(self.compose_tab, text="Compose Email")

        self.setup_inbox_ui()
        self.setup_compose_ui()

        self.logout_btn = tk.Button(self, text="Logout", command=self.logout_user)
        self.logout_btn.pack(pady=10)

    def logout_user(self):
        """Logout the user from the application"""
        self.controller.current_user = None
        self.controller.current_user_key = None  # Wipe the key from memory on logout
        self.controller.show_frame("LoginFrame")

    def on_show(self):
        """Triggers automatically when switching to the dashboard frame"""
        # 1. Update the top status bar with the new user's information
        self.user_label.config(text=f"Active User Account: {self.controller.current_user}")
        # 2. reset treeview to fetch new user's email
        self.refresh_inbox()
        # 3. Update  the recipient list combo menu
        self.update_recipient_dropdown()
        self.crypto_status_lbl.config(text = "Status: Waiting for selection...", fg = "orange")

        self.display_text.config(state="normal")  # Temporarily unlock widget to edit text
        self.display_text.delete("1.0", tk.END)  # Wipe out the previous user's decrypted text
        self.display_text.config(state="disabled")  # Re-lock the widget to keep it read-only

    def update_recipient_dropdown(self):
        """Fetches all registered users from the DB and excludes the current logged-in user."""
        conn = sqlite3.connect("email_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username != ?", (self.controller.current_user,))
        users = [row[0] for row in cursor.fetchall()]
        conn.close()  # Dynamically inject the array list into the combobox containerself.recip_combo['values'] = users
        self.recip_combo['values'] = users

    def setup_inbox_ui(self):
        """Sets up the inbox ui"""
        left_pane = tk.Frame(self.inbox_tab)
        left_pane.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.title_lbl = tk.Label(left_pane, text="Select an email to decrypt:", font=("Arial", 10, "bold"))
        self.title_lbl.pack(anchor="w")

        self.email_tree = ttk.Treeview(left_pane, columns=("Sender", "Subject"), show="headings", height=15)
        self.email_tree.heading("Sender", text="From Sender")
        self.email_tree.heading("Subject", text="Subject Title")
        self.email_tree.column("Sender", width=120)
        self.email_tree.column("Subject", width=180)
        self.email_tree.pack(fill="both", expand=True, pady=5)
        self.email_tree.bind("<<TreeviewSelect>>", self.on_email_clicked)

        right_pane = tk.Frame(self.inbox_tab)
        right_pane.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.decrypt_lbl = tk.Label(right_pane, text="Decryption Output Details:", font=("Arial", 10, "bold"))
        self.decrypt_lbl.pack(anchor="w")

        self.crypto_status_lbl = tk.Label(right_pane, text="Status: Waiting for selection...", fg="orange",
                                          wraplength=250)
        self.crypto_status_lbl.pack(anchor="w", pady=2)

        self.msg_lbl = tk.Label(right_pane, text="Decrypted Message Body:")
        self.msg_lbl.pack(anchor="w", pady=(10, 2))
        self.display_text = tk.Text(right_pane, wrap="word", width=35, height=12, bg="#f4f4f4")
        self.display_text.pack(fill="both", expand=True)
        self.display_text.config(state="disabled")

    def refresh_inbox(self):
        """Refreshes the inbox ui"""
        for row in self.email_tree.get_children():
            self.email_tree.delete(row)

        conn = sqlite3.connect("email_app.db")
        cursor = conn.cursor()
        # View emails sent *to* this specific user
        cursor.execute("SELECT id, sender, subject FROM emails WHERE recipient = ?", (self.controller.current_user,))

        for email_id, sender, subject in cursor.fetchall():
            self.email_tree.insert("", "end", iid=str(email_id), values=(sender, subject))
        conn.close()

    def on_email_clicked(self, event):
        """Triggers when an email is clicked, displays the selected email"""
        selected_item = self.email_tree.selection()
        if not selected_item:
            return

        email_id = selected_item[0]

        conn = sqlite3.connect("email_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_body, sender, recipient FROM emails WHERE id = ?", (email_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            encrypted_payload = row[0]
            sender = row[1]
            recipient = row[2]

            try:
                # Attempt standard decryption with the current session key
                cipher_suite = Fernet(self.controller.current_user_key)
                decrypted_bytes = cipher_suite.decrypt(encrypted_payload)
                decrypted_message = decrypted_bytes.decode('utf-8')

                self.crypto_status_lbl.config(text="Status: Decrypted successfully!", fg="green")
                self.display_text.config(state="normal")
                self.display_text.delete("1.0", tk.END)
                self.display_text.insert("1.0", decrypted_message)
                self.display_text.config(state="disabled")

            except InvalidToken:
                # Checks for malicious attack or desynchronisation of keys

                is_tampered = False
                try:
                    # Fernet tokens have strict padding and encoding structures.
                    if len(encrypted_payload) < 50:
                        is_tampered = True

                    if list(encrypted_payload)[0] != 128:
                        is_tampered = True
                except Exception:
                    is_tampered = True

                # Clear display text area
                self.display_text.config(state="normal")
                self.display_text.delete("1.0", tk.END)
                self.display_text.config(state="disabled")

                if is_tampered:
                    self.crypto_status_lbl.config(
                        text="CRITICAL ALERT: Message Integrity Failure! The ciphertext data has been maliciously altered.",
                        fg="red"
                    )
                else:
                    self.crypto_status_lbl.config(
                        text="CONFIGURATION ERROR: Cryptographic Key Mismatch! \nThe file integrity is intact, but you do not hold the correct key to open it.",
                        fg="orange"
                    )

    def setup_compose_ui(self):
        """Function for setting up compose email ui"""
        self.recip_lbl = tk.Label(self.compose_tab, text="Recipient Username:")
        self.recip_lbl.pack(anchor="w", padx=20, pady=(10, 2))

        self.recip_combo = ttk.Combobox(self.compose_tab, width = 47)
        self.recip_combo.pack(padx=20, pady=2)

        self.subject_lbl = tk.Label(self.compose_tab, text="Subject Line:")
        self.subject_lbl.pack(anchor="w", padx=20, pady=2)
        self.sub_entry = tk.Entry(self.compose_tab, width=50)
        self.sub_entry.pack(padx=20, pady=2)

        self.body_lbl = tk.Label(self.compose_tab, text="Message Body:")
        self.body_lbl.pack(anchor="w", padx=20, pady=2)
        self.body_text = tk.Text(self.compose_tab, wrap="word", width=50, height=10)
        self.body_text.pack(padx=20, pady=2)

        self.send_btn = tk.Button(self.compose_tab, text="Encrypt with Recipient's Key & Send", bg="#008CBA", fg="white", command=self.send_email)
        self.send_btn.pack(pady=15)

    def send_email(self):
        """Function for sending email"""
        recipient = self.recip_combo.get().strip()
        subject = self.sub_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()

        if not recipient or not subject or not body:
            messagebox.showwarning("Incomplete", "Please fill out all fields.")
            return

        # Fetch the recipient's encryption salt from the DB to derive THEIR key
        conn = sqlite3.connect("email_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT crypto_salt FROM users WHERE username = ?", (recipient,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Error",
                                 f"Recipient '{recipient}' does not exist. They must register an account first.")
            conn.close()
            return

        recipient_salt = row[0]

        try:
            recipient_mock_passphrase = f"{recipient}_secured_passphrase"
            recipient_key = derive_user_key(recipient_mock_passphrase, recipient_salt)

            cipher_suite = Fernet(recipient_key)
            encrypted_blob = cipher_suite.encrypt(body.encode('utf-8'))

            cursor.execute("INSERT INTO emails (sender, recipient, subject, encrypted_body) VALUES (?, ?, ?, ?)",
                           (self.controller.current_user, recipient, subject, encrypted_blob))
            conn.commit()
            messagebox.showinfo("Encrypted & Sent",
                                f"Message successfully encrypted using {recipient}'s unique salt architecture!")
        except Exception as e:
            messagebox.showerror("Crypto Error", f"Failed to encrypt: {str(e)}")
        finally:
            conn.close()

        # Clears the entry boxes
        self.recip_combo.set("")
        self.sub_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        self.refresh_inbox()
        self.notebook.select(0)


if __name__ == "__main__":
    init_db() # Initializes the database
    app = EmailApp()
    app.mainloop()

