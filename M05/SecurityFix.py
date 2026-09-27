# SecurityFix.py
# Jennifer Bowers
# Module 5: Assignment - OWASP Top 10 Code Fix
# 9/25/2026

# A good portion of the assignment was explained to me by AI as I didn't understand other coding languages besides Python.

# # Broken Access Control
# # 1. 

# app.get('/profile/:userId', (req, res) => {
#     User.findById(req.params.userId, (err, user) => {
#         if (err) return res.status(500).send(err);
#         res.json(user);
#     });
# });

# # ---Reason---
# # This method leaks possible database information through the error message which can help a hacker figure out how to crack through the flaw. It also allows DoS explotation.

# # ----Fix---
# # Created with the help of AI
# @app.get('/profile/:userId', async (req, res) => {
#     try{
#         if (!mongoose.Types.ObjectId.isValid(req.params.userId)) {
#             return res.status(400).send('Invalid User ID format');
#         }
#         const user = await User.findById(req.params.userId);
#         if (!user){
#             return res.status(404).send('User not found');
#         }
#         res.jason(user);
#     } catch(err) {
#         res.status(500).send('Server Error');
#     }
# });

# #-------------------------------------

# # 2. 

# @app.route('/account/<user_id>')
# def get_account(user_id):
#     user = db.query(User).filter_by(id=user_id).first()
#     return jsonify(user.to_dict())

# # ---Reason---
# # Assumes a user ALWAYS exists, thus easy to crash the server if an id isn't in the database. "Null pointer crash"

# # ----Fix---
# # Created with the help of AI
# @app.route('/account/<user_id>')
# def get_account(user_id):
#     user = db.query(User).filter_by(id = user_id).first()

#     if user is None:
#         return jsonify({"Error": "User not found"}), 404
#     return jsonify(user.to_dict())

# #-------------------------------------

# # Cryptographic Failures
# # 3.

# public String hashPassword(String password) throws NoSuchAlgorithmException {
#     MessageDigest md = MessageDigest.getInstance("MD5");
#     md.update(password.getBytes());
#     byte[] digest = md.digest();
#     return DatatypeConverter.printHexBinary(digest);
# }

# # ---Reason---
# # MD5 is designed for checking errors and is not secure for passwords. Brute force and rainbow tables are possible exploits. It also has no salt. Fix this by using bcrypt, sha-256, and salts.

# # ----Fix---
# # Created with the help of AI
# public String hashPassword(String password) {
#     return BCrypt.hashpw(password, BCrypt.gensalt());
# }


# #-------------------------------------


# # 4.

# # import hashlib

# def hash_password(password):
#     return hashlib.sha1(password.encode()).hexdigest()

# # ---Reasoning---
# # First off, hashing via sha1 is not secure enough for passwords. Use a slower sha-256 and add a salt. Start with pip install bcrypt

# # ----Fix---
# import bcrypt

# def hash_password(password):
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode(), salt)



# #-------------------------------------


# # Injection
# # 5.

# String username = request.getParameter("username");
# String query = "SELECT * FROM users WHERE username = '" + username + "'";
# Statement stmt = connection.createStatement();
# ResultSet rs = stmt.executeQuery(query);

# # ---Reasoning---
# # SQL Injection is possible with the input capable of passing commands. The input needs sanitized before passing into a prepared statement, passing the input as a parameter as a literal string and not an executable command.

# # ----Fix---
# # Created with the help of AI
# String username = request.getParameter("username");
# String query = "SELECT * FROM users WHERE username = ?";
# PreparedStatement pstmt = connection.preparedStatement(query);
# pstmt.setString(1, username);
# ResultSet rs = pstmt.executeQuery();


# #-------------------------------------

# # 6. 

# app.get('/user', (req, res) => {
#     // Directly trusting query parameters can lead to NoSQL injection
#     db.collection('users').findOne({ username: req.query.username }, (err, user) => {
#         if (err) throw err;
#         res.json(user);
#     });
# });
# # ---Reasoning---
# # Object injection exploit. Even though the code points out the error, it still runs the command which can bypass authentication and extract private data.

# # ----Fix---
# # Created with the help if AI
# app.get('/user', (req, res) => {
#     const searchUsername = String(req.query.username);
#     db.collection('users').findOne({ username: searchUsername }, (err, user) =>{
#         if (err) return res.stsatus(500).send("Database error");
#         if (!user) return res.status(404).send("User not found");
#         res.json(user);
#     });
# });


# #-------------------------------------

# # Insecure Design
# # 7.

# @app.route('/reset-password', methods=['POST'])
# def reset_password():
#     email = request.form['email']
#     new_password = request.form['new_password']
#     user = User.query.filter_by(email=email).first()
#     user.password = new_password
#     db.session.commit()
#     return 'Password reset'
# # ---Reasoning---
# # This flaw allows anyone to someone else's password just by knowing the email address alone. There is no verification process. Fix it by adding validation and secret tokens. This code will also crash should an email be passed that doesn't exist as well as no hashing (passwords are saved in plain text in the database). The fix to this is to send a secret token to the user's email with an expiration time then accepting a new password as long as the email and token match and not expired.

# # ----Fix---
# import secrets
# from datetime import datetime, timedelta
# import bcrypt

# # First send a token to the person's email to reset the password
# @app.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     email = request.form['email']
#     user = User.query.filter_by(email=email).first()
    
#     # Send a email to the user's email (if it exists)
#     if user:
#         # Create a random unique token
#         token = secrets.token_urlsafe(32)
        
#         # Save token and a 15 minute expiration time to the account
#         user.reset_token = token
#         user.token_expiry = datetime.utcnow() + timedelta(minutes=15)
#         db.session.commit()
        
#         # Email the link containing the token to the user's actual inbox
#         send_reset_email(user.email, token)
        
#     return 'If that account exists, a reset link has been sent.'

# # Next allow changing of the password
# @app.route('/reset-password/<token>', methods = ['POST'])
# def reset_password(token):
#     # Gather new password
#     new_password = request.form['new_password']
#     # Confirm that the token matches the user and the token is not expired
#     user = User.query.filter_by(reset_token = token).first():
#     if not user or user.token_expiry, datetime.utcnow():
#         return "Invalid or expired token", 400
#     # Encode the password
#     password_bytes = new_password.encode('utf-8')
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password_bytes, salt)

#     # Commit to the database
#     user.password = str(hashed_password.decode('utf-8')) # Saves to a string before commiting to the datbase
#     user.reset_token = None # Resets the token
#     user.token_expiry = None # Resets the token datetime
#     db.session.commit()

#     return "Password updated successfully"

# #-------------------------------------

# # Software and Data Integrity Failures
# # 8.

# <script src="https://cdn.example.com/lib.js"></script>

# # ---Reason---
# # This is a third party supply chain attack exploit. In otherwords, it assumes that the address will never be hacked, altered, or otherwise compromised. To fix this, set a fingerprint to the expected file and refuse to run it if it doesnt perfectly match.

# # ----Fix---
# # Created with the help if AI
# <!-- SECURE: Explicitly verifies the file hash before running -->
# <script 
#   src="https://cdn.example.com/lib.js" 
#   integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC" 
#   crossorigin="anonymous">
# </script>

# #-------------------------------------

# # Server-Side Request Forgery
# # 9.

# url = input("Enter URL: ")
# response = requests.get(url)
# print(response.text)

# # ---Reasoning---
# # Getting and running the url directly allows hackers to exploit the server-side request forgery exploit. Meaning it allows hackers to see the private side of the server, the internal network where the database, internal services, and others reside. Fix this by creating an allowlist to restrict accessable urls.

# # ----Fix---
# import requests
# from urllib.parse import urlparse

# ALLOWED_DOMAINS = {"://ivytech.edu", "://github.com"}
# url = input("Enter URL: ")
# parsed_url = urlparse(url)

# # Enforce HTTPS only
# if parsed_url.scheme != "https":
#     print("Error: Only HTTPS links are allowed.")
#     exit()
# # Check for allowed domain
# if parsed_url.netloc not in ALLOWED_DOMAINS:
#     print("Error: Untrusted Domain.")
#     exit()
# response = requests.get(url)
# print(response.text)

# #-------------------------------------

# # Identification and Authentication Failures
# # 10.

# if (inputPassword.equals(user.getPassword())) { 
#     // Login success
# }
# # ---Reasoning---
## This demostrates that passwords are stored in plain text so hackers are able to guess, character by character, based on how long it takes the database to respond. Fix this by always encrypting passwords before storing them.

# # ----Fix---
## Created with the help of AI
# // Bcrypt automatically hashes and compares passwords along with a constant-time check to prevent timing attacks
# if (Bcrypt.checkpw(inputPassword, user.getPasswordHash())) {
#     // Login success
# } else {
#     // Login Failure
# }



