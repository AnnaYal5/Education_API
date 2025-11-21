import hashlib

class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        "Хешування паролю"
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        "Перевірка паролю"
        return Hasher.hash_password(password) == password_hash