from __future__ import annotations
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

_pwd_context = PasswordHash((Argon2Hasher(),))

def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password:str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)

def needs_rehash(hashed_password: str) -> bool:
    """True if the stored hash was made with an outdated scheme/work-factory
    and should be re-hashed on next successful login"""
    
    return _pwd_context.needs_update(hashed_password)