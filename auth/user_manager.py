# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from database.models import User
from auth.password_utils import hash_password, verify_password, is_password_strong
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class UserManager:
    """Klasa zarządzająca użytkownikami w systemie."""
    
    @staticmethod
    def register_user(username, email, password):
        """
        Rejestruje nowego użytkownika w systemie.
        Zwraca (User, None) w przypadku sukcesu lub (None, error_message) w przypadku błędu.
        """
        # Sprawdzenie czy użytkownik o takiej nazwie już istnieje
        existing_user = User.get_by_username(username)
        if existing_user:
            return None, "Użytkownik o takiej nazwie już istnieje."
        
        # Sprawdzenie czy email jest już używany
        existing_email = User.get_by_email(email)
        if existing_email:
            return None, "Ten adres email jest już używany."
        
        # Sprawdzenie siły hasła
        if not is_password_strong(password):
            return None, "Hasło nie spełnia wymagań bezpieczeństwa."
        
        # Haszowanie hasła
        password_hash, salt = hash_password(password)
        
        # Tworzenie nowego użytkownika
        user = User()
        user.username = username
        user.email = email
        user.password_hash = password_hash
        user.salt = salt
        user.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.is_admin = False
        user.is_active = True
        
        # Zapisanie użytkownika w bazie
        user_id = user.save()
        if not user_id:
            return None, "Nie udało się utworzyć konta. Spróbuj ponownie później."
        
        # Inicjalizacja statystyk użytkownika
        with DatabaseManager() as db:
            db.insert('user_stats', {'user_id': user_id})
            db.insert('user_streaks', {'user_id': user_id})
        
        logger.info(f"Zarejestrowano nowego użytkownika: {username}")
        return user, None
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Uwierzytelnia użytkownika na podstawie nazwy użytkownika i hasła.
        Zwraca (User, None) w przypadku sukcesu lub (None, error_message) w przypadku błędu.
        """
        # Pobieranie użytkownika
        user = User.get_by_username(username)
        if not user:
            return None, "Nieprawidłowa nazwa użytkownika lub hasło."
        
        # Sprawdzenie czy konto jest aktywne
        if not user.is_active:
            return None, "Konto zostało dezaktywowane."
        
        # Weryfikacja hasła
        if not verify_password(password, user.password_hash, user.salt):
            return None, "Nieprawidłowa nazwa użytkownika lub hasło."
        
        # Aktualizacja daty ostatniego logowania
        user.update_last_login()
        
        logger.info(f"Użytkownik {username} zalogował się")
        return user, None
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Zmienia hasło użytkownika.
        Zwraca (True, None) w przypadku sukcesu lub (False, error_message) w przypadku błędu.
        """
        # Pobieranie użytkownika
        user = User.get_by_id(user_id)
        if not user:
            return False, "Użytkownik nie istnieje."
        
        # Weryfikacja starego hasła
        if not verify_password(old_password, user.password_hash, user.salt):
            return False, "Nieprawidłowe aktualne hasło."
        
        # Sprawdzenie siły nowego hasła
        if not is_password_strong(new_password):
            return False, "Nowe hasło nie spełnia wymagań bezpieczeństwa."
        
        # Haszowanie nowego hasła
        password_hash, salt = hash_password(new_password)
        
        # Aktualizacja hasła
        user.password_hash = password_hash
        user.salt = salt
        user.save()
        
        logger.info(f"Zmieniono hasło dla użytkownika {user.username}")
        return True, None
    
    @staticmethod
    def reset_password(email):
        """
        Resetuje hasło użytkownika i generuje tymczasowe.
        W rzeczywistej aplikacji wysłałoby email z linkiem do resetowania.
        Na potrzeby tego przykładu zwraca nowe hasło.
        """
        # Pobieranie użytkownika
        user = User.get_by_email(email)
        if not user:
            return None, "Nie znaleziono użytkownika o podanym adresie email."
        
        # Generowanie tymczasowego hasła
        import random
        import string
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # Haszowanie tymczasowego hasła
        password_hash, salt = hash_password(temp_password)
        
        # Aktualizacja hasła
        user.password_hash = password_hash
        user.salt = salt
        user.save()
        
        logger.info(f"Zresetowano hasło dla użytkownika {user.username}")
        
        # W rzeczywistej aplikacji wysyłamy email z linkiem do resetowania
        # Tutaj zwracamy tymczasowe hasło dla przykładu
        return temp_password, None
    
    @staticmethod
    def update_profile(user_id, email=None, username=None):
        """
        Aktualizuje profil użytkownika.
        Zwraca (True, None) w przypadku sukcesu lub (False, error_message) w przypadku błędu.
        """
        # Pobieranie użytkownika
        user = User.get_by_id(user_id)
        if not user:
            return False, "Użytkownik nie istnieje."
        
        # Sprawdzenie czy nowa nazwa użytkownika jest dostępna
        if username and username != user.username:
            existing_user = User.get_by_username(username)
            if existing_user:
                return False, "Użytkownik o takiej nazwie już istnieje."
            user.username = username
        
        # Sprawdzenie czy nowy email jest dostępny
        if email and email != user.email:
            existing_email = User.get_by_email(email)
            if existing_email:
                return False, "Ten adres email jest już używany."
            user.email = email
        
        # Zapisanie zmian
        user.save()
        
        logger.info(f"Zaktualizowano profil użytkownika {user.username}")
        return True, None