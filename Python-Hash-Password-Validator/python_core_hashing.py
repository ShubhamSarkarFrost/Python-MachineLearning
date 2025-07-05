import sqlite3
import hashlib # Re-import hashlib for PBKDF2
import os # Still needed for os.urandom for salt generation
import base64
from cryptography.fernet import Fernet, InvalidToken
import random
import string
# import bcrypt # Removed bcrypt import

# --- Configuration ---
DB_NAME = 'password_manager.db'
MASTER_KEY_TABLE = 'master_key'
PASSWORDS_TABLE = 'passwords'

# --- Database Utilities ---
def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def setup_database():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for storing the hashed master password and salt (re-added salt column)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {MASTER_KEY_TABLE} (
            id INTEGER PRIMARY KEY,
            hashed_master_password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')

    # Table for storing encrypted passwords
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {PASSWORDS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Hashing and Encryption Utilities ---
def hash_password(password, salt=None):
    """Hashes a password using SHA256 with a salt (PBKDF2_HMAC)."""
    if salt is None:
        salt = os.urandom(16) # Generate a new 16-byte random salt
    else:
        salt = base64.b64decode(salt) # Decode existing salt from base64

    # Combine password and salt, then hash
    hashed_pwd = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000 # Number of iterations (higher is more secure but slower)
    )
    return base64.b64encode(hashed_pwd).decode('utf-8'), base64.b64encode(salt).decode('utf-8')

def derive_fernet_key(master_pwd):
    """Derives a Fernet encryption key from the master password."""
    # Use SHA256 hash of the master password as the base for the Fernet key
    # Fernet keys must be 32 URL-safe base64-encoded bytes.
    # SHA256 produces 32 bytes, which is perfect.
    key_material = hashlib.sha256(master_pwd.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(key_material)

class PasswordEncryptor:
    """Handles encryption and decryption of passwords using Fernet."""
    def __init__(self, master_pwd):
        self.key = derive_fernet_key(master_pwd)
        self.f = Fernet(self.key)

    def encrypt(self, data):
        """Encrypts data."""
        return self.f.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, encrypted_data):
        """Decrypts data."""
        try:
            return self.f.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
        except InvalidToken:
            # In a GUI context, the GUI layer should handle the messagebox.
            # Here, we just return None to indicate failure.
            return None

# --- Password Generator Utility ---
def generate_password(length=12, use_digits=True, use_symbols=True, use_uppercase=True, use_lowercase=True):
    """Generates a random strong password."""
    characters = ""
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "" # No character sets selected

    password = ''.join(random.choice(characters) for i in range(length))
    return password

# --- Core Logic Functions for GUI interaction ---

def check_master_password_exists():
    """Checks if a master password has been set in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {MASTER_KEY_TABLE}")
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def set_new_master_password(new_pwd):
    """Sets a new master password in the database."""
    hashed_pwd, salt = hash_password(new_pwd) # hash_password now returns hash and salt
    conn = get_db_connection()
    cursor = conn.cursor()
    # Store both the hashed password and the salt
    cursor.execute(f"INSERT INTO {MASTER_KEY_TABLE} (hashed_master_password, salt) VALUES (?, ?)",
                   (hashed_pwd, salt))
    conn.commit()
    conn.close()

def verify_master_password(entered_pwd):
    """Verifies the entered master password against the stored hash and salt."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT hashed_master_password, salt FROM {MASTER_KEY_TABLE}")
    master_data = cursor.fetchone()
    conn.close()

    if master_data:
        stored_hash = master_data['hashed_master_password']
        stored_salt = master_data['salt']

        hashed_entered_pwd, _ = hash_password(entered_pwd, stored_salt) # Use stored_salt for hashing entered_pwd

        return hashed_entered_pwd == stored_hash
    return False

def add_password_entry(encryptor, website, username, password):
    """Adds an encrypted password entry to the database."""
    encrypted_pwd = encryptor.encrypt(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {PASSWORDS_TABLE} (website, username, encrypted_password) VALUES (?, ?, ?)",
                   (website, username, encrypted_pwd))
    conn.commit()
    conn.close()

def get_all_password_entries():
    """Retrieves all password entries (website and username) from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, website, username FROM {PASSWORDS_TABLE}")
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_encrypted_password_by_id(entry_id):
    """Retrieves the encrypted password for a given entry ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT encrypted_password FROM {PASSWORDS_TABLE} WHERE id = ?", (entry_id,))
    encrypted_pwd_data = cursor.fetchone()
    conn.close()
    return encrypted_pwd_data['encrypted_password'] if encrypted_pwd_data else None

def delete_password_entry_by_id(entry_id):
    """Deletes a password entry from the database by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {PASSWORDS_TABLE} WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

# Initialize the database when the core module is imported
setup_database()
