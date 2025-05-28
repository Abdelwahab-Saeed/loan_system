import bcrypt
from db import DatabaseManager 
import getpass  

class User:
    def __init__(self):
        self.db = DatabaseManager()

    def hash_password(self, plain_password: str) -> bytes:
        # Important -> bcrypt requires bytes
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed

    def check_password(self, plain_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    def register(self, username: str, password: str) -> bool:
        # Check if user already exists
        self.db.execute("SELECT id FROM users WHERE username = %s", (username,))
        if self.db.fetchone():
            print("Username already exists.")
            return False
        
        hashed = self.hash_password(password)
        self.db.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed.decode('utf-8'))  # store as string
        )
        print("Registration successful!")
        return True

    def login(self, username: str, password: str):
        self.db.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        result = self.db.fetchone()
        if not result:
            print("Username not found.")
            return None  # Explicitly return None if login fails

        user_id, stored_hash = result
        if self.check_password(password, stored_hash.encode('utf-8')):
            print(f"Welcome back, {username}!")
            return user_id  # ✅ Return the actual user_id
        else:
            print("Incorrect password.")
            return None


    def close(self):
        self.db.close()
