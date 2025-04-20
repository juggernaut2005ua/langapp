# -*- coding: utf-8 -*-

import logging
from database.models import User
from datetime import datetime, timedelta
from config import TOKEN_EXPIRY_DAYS

logger = logging.getLogger(__name__)

class LoginManager:
    """Klasa zarządzająca sesją zalogowanego użytkownika."""
    
    _current_user = None
    _login_timestamp = None
    
    @classmethod
    def login(cls, user):
        """
        Zapisuje obecnie zalogowanego użytkownika.
        """
        cls._current_user = user
        cls._login_timestamp = datetime.now()
        logger.debug(f"Zalogowano użytkownika: {user.username}")
    
    @classmethod
    def logout(cls):
        """
        Wylogowuje obecnie zalogowanego użytkownika.
        """
        if cls._current_user:
            logger.debug(f"Wylogowano użytkownika: {cls._current_user.username}")
            cls._current_user = None
            cls._login_timestamp = None
    
    @classmethod
    def get_current_user(cls):
        """
        Zwraca obecnie zalogowanego użytkownika lub None.
        """
        # Sprawdzenie czy sesja nie wygasła
        if cls._current_user and cls._login_timestamp:
            expiry_time = cls._login_timestamp + timedelta(days=TOKEN_EXPIRY_DAYS)
            if datetime.now() > expiry_time:
                logger.debug("Sesja użytkownika wygasła, wylogowywanie...")
                cls.logout()
                return None
        
        return cls._current_user
    
    @classmethod
    def is_authenticated(cls):
        """
        Sprawdza czy użytkownik jest zalogowany.
        """
        return cls.get_current_user() is not None
    
    @classmethod
    def is_admin(cls):
        """
        Sprawdza czy zalogowany użytkownik jest administratorem.
        """
        user = cls.get_current_user()
        return user is not None and user.is_admin
    
    @classmethod
    def refresh_session(cls):
        """
        Odświeża timestamp sesji użytkownika.
        """
        if cls._current_user:
            cls._login_timestamp = datetime.now()
            logger.debug(f"Odświeżono sesję użytkownika: {cls._current_user.username}")