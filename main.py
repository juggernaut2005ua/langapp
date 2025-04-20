#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ui.login_window import LoginWindow
from database.db_setup import ensure_db_exists
from utils.logger import setup_logger
from config import APP_NAME, APP_VERSION, LOGO_PATH

def main():
    """Główna funkcja aplikacji, inicjalizuje wszystkie komponenty i uruchamia aplikację."""
    # Konfiguracja loggera
    setup_logger()
    logging.info(f"Uruchamianie {APP_NAME} v{APP_VERSION}")
    
    # Upewniamy się, że baza danych istnieje
    try:
        ensure_db_exists()
    except Exception as e:
        logging.critical(f"Błąd podczas inicjalizacji bazy danych: {e}")
        sys.exit(1)
    
    # Inicjalizacja aplikacji Qt
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(LOGO_PATH))
    
    # Ustawienie stylu aplikacji
    from ui.styles import set_application_style
    set_application_style(app)
    
    # Tworzenie i wyświetlanie okna logowania
    login_window = LoginWindow()
    login_window.show()
    
    # Uruchomienie pętli zdarzeń aplikacji
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()