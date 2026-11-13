import secrets
import hashlib
from passlib.context import CryptContext

context = CryptContext(schemes=["pbkdf2_sha256"])

def hash_text(text: str) -> str:
    return context.hash(text)

def verify_text(plain_text: str, text: str) -> bool:
    return context.verify(plain_text, text)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("UTF-8")).hexdigest()

def create_hashed_token() -> str:
    return hash_token(secrets.token_urlsafe(32))