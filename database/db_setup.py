# -*- coding: utf-8 -*-

import os
import sqlite3
import logging
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

def ensure_db_exists():
    """Sprawdza czy baza danych istnieje, jeśli nie - tworzy ją."""
    db_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    if not os.path.exists(DATABASE_PATH):
        logger.info(f"Tworzenie nowej bazy danych w: {DATABASE_PATH}")
        create_database()
    else:
        logger.info(f"Baza danych już istnieje w: {DATABASE_PATH}")
        # Opcjonalnie można dodać sprawdzenie wersji schematu i migrację
        
def create_database():
    """Tworzy bazę danych i wszystkie potrzebne tabele."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Tabela użytkowników
        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_admin BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        # Tabela języków
        cursor.execute('''
        CREATE TABLE languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        # Tabela kategorii lekcji
        cursor.execute('''
        CREATE TABLE lesson_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            language_id INTEGER,
            FOREIGN KEY (language_id) REFERENCES languages (id)
        )
        ''')
        
        # Tabela lekcji
        cursor.execute('''
        CREATE TABLE lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            language_id INTEGER,
            difficulty INTEGER DEFAULT 1,
            xp_reward INTEGER DEFAULT 10,
            order_index INTEGER,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES lesson_categories (id),
            FOREIGN KEY (language_id) REFERENCES languages (id)
        )
        ''')
        
        # Tabela ćwiczeń
        cursor.execute('''
        CREATE TABLE exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options TEXT,
            hint TEXT,
            image_path TEXT,
            audio_path TEXT,
            xp_reward INTEGER DEFAULT 5,
            order_index INTEGER,
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
        ''')
        
        # Tabela postępów użytkownika
        cursor.execute('''
        CREATE TABLE user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            completed BOOLEAN DEFAULT 0,
            completion_date TIMESTAMP,
            score INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
        ''')
        
        # Tabela odznak/osiągnięć
        cursor.execute('''
        CREATE TABLE achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            requirement TEXT NOT NULL,
            xp_reward INTEGER DEFAULT 20
        )
        ''')
        
        # Tabela osiągnięć użytkownika
        cursor.execute('''
        CREATE TABLE user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_id INTEGER,
            earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (achievement_id) REFERENCES achievements (id)
        )
        ''')
        
        # Tabela streaka (codziennej aktywności)
        cursor.execute('''
        CREATE TABLE user_streaks (
            user_id INTEGER PRIMARY KEY,
            current_streak INTEGER DEFAULT 0,
            max_streak INTEGER DEFAULT 0,
            last_activity_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Tabela statystyk użytkownika
        cursor.execute('''
        CREATE TABLE user_stats (
            user_id INTEGER PRIMARY KEY,
            total_xp INTEGER DEFAULT 0,
            lessons_completed INTEGER DEFAULT 0,
            exercises_completed INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            incorrect_answers INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Tabela ulubionych słówek użytkownika
        cursor.execute('''
        CREATE TABLE user_favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            language_id INTEGER,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (language_id) REFERENCES languages (id)
        )
        ''')
        
        # Zapisanie zmian
        conn.commit()
        logger.info("Utworzono bazę danych z wszystkimi tabelami")
        
        # Dodanie podstawowych danych
        insert_initial_data(conn)
        
        conn.close()
    except Exception as e:
        logger.error(f"Błąd podczas tworzenia bazy danych: {e}")
        raise

def insert_initial_data(conn):
    """Dodaje podstawowe dane do bazy."""
    cursor = conn.cursor()
    
    # Dodanie podstawowych języków
    languages = [
        ('en', 'English'),
        ('pl', 'Polski'),
        ('es', 'Español'),
        ('de', 'Deutsch'),
        ('fr', 'Français'),
        ('ru', 'Русский')
    ]
    
    cursor.executemany(
        'INSERT INTO languages (code, name) VALUES (?, ?)',
        languages
    )
    
    # Dodanie administratora (hasło: admin123)
    from auth.password_utils import hash_password
    password_hash, salt = hash_password('admin123')
    
    cursor.execute(
        'INSERT INTO users (username, email, password_hash, salt, is_admin) VALUES (?, ?, ?, ?, ?)',
        ('admin', 'admin@lingualeap.com', password_hash, salt, 1)
    )
    
    # Dodanie podstawowych osiągnięć
    achievements = [
        ('Początkujący', 'Ukończ swoją pierwszą lekcję', 'beginner.png', 'lessons_completed >= 1', 10),
        ('Pilny uczeń', 'Osiągnij streak 7 dni', 'diligent.png', 'current_streak >= 7', 50),
        ('Poliglota', 'Zacznij naukę 3 różnych języków', 'polyglot.png', 'languages_started >= 3', 100)
    ]
    
    cursor.executemany(
        'INSERT INTO achievements (name, description, image_path, requirement, xp_reward) VALUES (?, ?, ?, ?, ?)',
        achievements
    )
    
    conn.commit()
    logger.info("Dodano podstawowe dane do bazy")