from cryptography.fernet import Fernet
import os

class SecurityManager:
    def __init__(self, key_file):
        self.key_file = key_file
        self.key = self._load_key()
        self.cipher = Fernet(self.key)

    def _load_key(self):
        """Loads existing key or generates a new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def encrypt_value(self, value):
        """Encrypts a float or string value."""
        if value is None:
            return None
        value_str = str(value)
        return self.cipher.encrypt(value_str.encode()).decode()

    def decrypt_value(self, encrypted_val):
        """Decrypts value back to string."""
        if not encrypted_val:
            return None
        return self.cipher.decrypt(encrypted_val.encode()).decode()