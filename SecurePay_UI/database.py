import sqlite3
import hashlib
import os

# Get absolute path to the database file
DB_PATH = os.path.abspath("users.db")

# Initialize database and ensure table structure is correct
def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                payment_status BOOLEAN DEFAULT 0  -- ✅ Ensuring 'payment_status' column exists
            )
        """)
        conn.commit()

# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add new user to the database
def add_user(username, email, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                raise ValueError("⚠️ Username or email already exists.")

            cursor.execute("INSERT INTO users (username, email, password, payment_status) VALUES (?, ?, ?, 0)",
                           (username, email, hash_password(password)))
            conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"⚠️ Database error: {str(e)}")

# Authenticate user login
def authenticate_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (username, hash_password(password)))
        return cursor.fetchone()  # Returns user data if exists

def update_payment_status(username):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        print(f"DEBUG: Updating payment status for {username} in DB")  # Debugging print
        cursor.execute("UPDATE users SET payment_status = 1 WHERE LOWER(username) = LOWER(?)", (username,))
        
        conn.commit()
        print(f"DEBUG: Database updated -> {username} payment_status = 1")  #Debug log
    except Exception as e:
        print(f"ERROR: Failed to update payment status for {username} -> {e}")  # Error handling
    finally:
        conn.close()

# ✅ Check if the user has made a payment
def has_paid(username):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payment_status FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return bool(result[0]) if result else False
    except sqlite3.Error as e:
        print(f"⚠️ Database error while checking payment status: {str(e)}")
        return False

# Initialize the database when the script runs
initialize_db()

