# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE

def setup_logger():
    """Konfiguruje globalny logger aplikacji."""
    log_level = getattr(logging, LOG_LEVEL.upper())
    
    # Upewnij się, że katalog z logami istnieje
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir) and log_dir:
        os.makedirs(log_dir)
    
    # Konfiguracja formatu logów
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Konfiguracja handlera dla pliku
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Konfiguracja handlera dla konsoli
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Konfiguracja głównego loggera
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = []  # Usunięcie istniejących handlerów
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def get_logger(name):
    """Zwraca logger z podaną nazwą."""
    return logging.getLogger(name)