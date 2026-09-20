# tamper_db.py
# Jennifer Bowers
# 9/16/2026

# This application simulates an attack on the database and prove that the app can detect a corrupted email
# After running email application at least once, log into bob_student (BobPass!99).
# Attempt to read the emails of bob_student again, one of them should flag as being a corrupted email.

import sqlite3

# Connect directly to your local application database file
conn = sqlite3.connect("email_app.db")
cursor = conn.cursor()

# 1. Fetch the most recent encrypted email blob from the table
cursor.execute("SELECT id, subject, encrypted_body FROM emails ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

if row:
    email_id, subject, encrypted_blob = row[0], row[1], row[2]
    print(f"Found target email ID {email_id}, subject header: {subject}. Original ciphertext snippet: {encrypted_blob[:20]}...")

    # 2. Corrupt exactly one byte of data in the encrypted payload
    mutable_blob = list(encrypted_blob)
    # Flip a single bit in the binary string structure
    mutable_blob[-1] = mutable_blob[-1] ^ 1
    tampered_blob = bytes(mutable_blob)

    # 3. Write the corrupted data back into the database
    cursor.execute("UPDATE emails SET encrypted_body = ? WHERE id = ?", (tampered_blob, email_id))
    conn.commit()
    print(f"Successfully tampered with email ID {email_id}, subject: {subject}! Database cell is now modified.")
else:
    print("Error: No emails found in the database. Please send one first.")

conn.close()