# -*- coding: utf-8 -*-

import os
import hashlib
import binascii
import logging
from config import PASSWORD_SALT_LENGTH, PASSWORD_HASH_METHOD

logger = logging.getLogger(__name__)

def generate_salt(length=PASSWORD_SALT_LENGTH):
    """Generuje losowy salt o określonej długości."""
    return binascii.hexlify(os.urandom(length)).decode()

def hash_password(password, salt=None):
    """
    Haszuje hasło z podanym salt lub generuje nowy salt.
    Zwraca hash hasła i użyty salt.
    """
    if salt is None:
        salt = generate_salt()
    
    # Łączymy hasło z salt i tworzymy hash
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    
    hash_obj = hashlib.new(PASSWORD_HASH_METHOD)
    hash_obj.update(password_bytes + salt_bytes)
    password_hash = hash_obj.hexdigest()
    
    return password_hash, salt

def verify_password(password, stored_hash, salt):
    """
    Weryfikuje czy podane hasło po zaszyfrowaniu z zapisanym
    salt daje taki sam hash jak zapisany hash.
    """
    calculated_hash, _ = hash_password(password, salt)
    return calculated_hash == stored_hash

def is_password_strong(password):
    """
    Sprawdza czy hasło jest wystarczająco silne.
    Zwraca True jeśli hasło jest silne, w przeciwnym razie False.
    """
    # Minimum 8 znaków
    if len(password) < 8:
        return False
    
    # Musi zawierać przynajmniej jedną cyfrę
    if not any(char.isdigit() for char in password):
        return False
    
    # Musi zawierać przynajmniej jedną małą literę
    if not any(char.islower() for char in password):
        return False
    
    # Musi zawierać przynajmniej jedną dużą literę
    if not any(char.isupper() for char in password):
        return False
    
    return True

def get_password_strength_message(password):
    """
    Zwraca komunikat o sile hasła i co trzeba poprawić.
    """
    messages = []
    
    if len(password) < 8:
        messages.append("Hasło musi mieć co najmniej 8 znaków.")
    
    if not any(char.isdigit() for char in password):
        messages.append("Hasło musi zawierać co najmniej jedną cyfrę.")
    
    if not any(char.islower() for char in password):
        messages.append("Hasło musi zawierać co najmniej jedną małą literę.")
    
    if not any(char.isupper() for char in password):
        messages.append("Hasło musi zawierać co najmniej jedną dużą literę.")
    
    if not messages:
        return "Hasło jest wystarczająco silne."
    else:
        return "\n".join(messages)