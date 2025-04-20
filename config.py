# -*- coding: utf-8 -*-

import os
from pathlib import Path

# Podstawowe informacje o aplikacji
APP_NAME = "LinguaLeap"
APP_VERSION = "1.0.0"

# Ścieżki katalogów
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
DATA_DIR = os.path.join(RESOURCES_DIR, "data")
IMAGES_DIR = os.path.join(RESOURCES_DIR, "images")
SOUNDS_DIR = os.path.join(RESOURCES_DIR, "sounds")

# Ścieżka do pliku bazy danych
DATABASE_PATH = os.path.join(BASE_DIR, "database", "lingualeap.db")

# Ścieżki do plików zasobów
LOGO_PATH = os.path.join(IMAGES_DIR, "logo.png")
LANGUAGES_FILE = os.path.join(DATA_DIR, "languages.json")

# Ustawienia bezpieczeństwa
PASSWORD_SALT_LENGTH = 32
PASSWORD_HASH_METHOD = "sha256"
TOKEN_EXPIRY_DAYS = 30

# Ustawienia aplikacji
DEFAULT_LANGUAGE = "en"  # Domyślny język interfejsu
MAX_LOGIN_ATTEMPTS = 5   # Maksymalna liczba nieudanych prób logowania
STREAK_RESET_HOURS = 36  # Liczba godzin, po których streak zostanie zresetowany

# Ustawienia systemowe
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, "lingualeap.log")

# Sprawdź czy katalogi istnieją, a jeśli nie - utwórz je
def ensure_directories_exist():
    dirs = [RESOURCES_DIR, DATA_DIR, IMAGES_DIR, SOUNDS_DIR]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

ensure_directories_exist()