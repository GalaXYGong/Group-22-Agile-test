from werkzeug.security import generate_password_hash, check_password_hash

# Test hashing and checking
password = "123456aA1!"
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
print(f"Hashed password: {hashed_password}")

# Check the password
password_check = check_password_hash(hashed_password, password)
print(f"Password check: {password_check}")

# Try checking with a wrong password
wrong_password_check = check_password_hash(hashed_password, "wrongpassword")
print(f"Wrong password check: {wrong_password_check}")
