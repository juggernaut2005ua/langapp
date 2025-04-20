# -*- coding: utf-8 -*-

from datetime import datetime
from database.db_manager import DatabaseManager

class BaseModel:
    """Bazowa klasa dla wszystkich modeli danych."""
    
    table_name = None
    
    def __init__(self, data=None):
        """Inicjalizuje model z opcjonalnymi danymi."""
        if data:
            for key, value in data.items():
                setattr(self, key, value)
    
    @classmethod
    def get_by_id(cls, id):
        """Pobiera obiekt po jego ID."""
        with DatabaseManager() as db:
            data = db.fetch_one(f"SELECT * FROM {cls.table_name} WHERE id = ?", (id,))
            return cls(data) if data else None
    
    @classmethod
    def get_all(cls):
        """Pobiera wszystkie obiekty danego typu."""
        with DatabaseManager() as db:
            data = db.fetch_all(f"SELECT * FROM {cls.table_name}")
            return [cls(item) for item in data]

class User(BaseModel):
    """Model reprezentujący użytkownika w systemie."""
    
    table_name = "users"
    
    def __init__(self, data=None):
        """Inicjalizuje użytkownika z danych z bazy."""
        self.id = None
        self.username = None
        self.email = None
        self.password_hash = None
        self.salt = None
        self.registration_date = None
        self.last_login = None
        self.is_admin = False
        self.is_active = True
        super().__init__(data)
    
    @classmethod
    def get_by_username(cls, username):
        """Pobiera użytkownika po nazwie użytkownika."""
        with DatabaseManager() as db:
            data = db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
            return cls(data) if data else None
    
    @classmethod
    def get_by_email(cls, email):
        """Pobiera użytkownika po adresie email."""
        with DatabaseManager() as db:
            data = db.fetch_one("SELECT * FROM users WHERE email = ?", (email,))
            return cls(data) if data else None
    
    def save(self):
        """Zapisuje lub aktualizuje użytkownika w bazie danych."""
        with DatabaseManager() as db:
            if self.id:
                data = {
                    'username': self.username,
                    'email': self.email,
                    'password_hash': self.password_hash,
                    'salt': self.salt,
                    'last_login': self.last_login,
                    'is_admin': self.is_admin,
                    'is_active': self.is_active
                }
                db.update('users', data, 'id = ?', (self.id,))
                return self.id
            else:
                data = {
                    'username': self.username,
                    'email': self.email,
                    'password_hash': self.password_hash,
                    'salt': self.salt,
                    'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'is_admin': self.is_admin,
                    'is_active': self.is_active
                }
                self.id = db.insert('users', data)
                return self.id
    
    def update_last_login(self):
        """Aktualizuje datę ostatniego logowania."""
        self.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with DatabaseManager() as db:
            db.update('users', {'last_login': self.last_login}, 'id = ?', (self.id,))
    
    def get_stats(self):
        """Pobiera statystyki użytkownika."""
        with DatabaseManager() as db:
            return db.fetch_one("SELECT * FROM user_stats WHERE user_id = ?", (self.id,))
    
    def get_streak(self):
        """Pobiera informacje o streaku użytkownika."""
        with DatabaseManager() as db:
            return db.fetch_one("SELECT * FROM user_streaks WHERE user_id = ?", (self.id,))

class Language(BaseModel):
    """Model reprezentujący język w systemie."""
    
    table_name = "languages"
    
    def __init__(self, data=None):
        """Inicjalizuje język z danych z bazy."""
        self.id = None
        self.code = None
        self.name = None
        self.is_active = True
        super().__init__(data)
    
    @classmethod
    def get_by_code(cls, code):
        """Pobiera język po jego kodzie."""
        with DatabaseManager() as db:
            data = db.fetch_one("SELECT * FROM languages WHERE code = ?", (code,))
            return cls(data) if data else None
    
    @classmethod
    def get_active(cls):
        """Pobiera wszystkie aktywne języki."""
        with DatabaseManager() as db:
            data = db.fetch_all("SELECT * FROM languages WHERE is_active = 1")
            return [cls(item) for item in data]
    
    def save(self):
        """Zapisuje lub aktualizuje język w bazie danych."""
        with DatabaseManager() as db:
            if self.id:
                data = {
                    'code': self.code,
                    'name': self.name,
                    'is_active': self.is_active
                }
                db.update('languages', data, 'id = ?', (self.id,))
                return self.id
            else:
                data = {
                    'code': self.code,
                    'name': self.name,
                    'is_active': self.is_active
                }
                self.id = db.insert('languages', data)
                return self.id

class Lesson(BaseModel):
    """Model reprezentujący lekcję w systemie."""
    
    table_name = "lessons"
    
    def __init__(self, data=None):
        """Inicjalizuje lekcję z danych z bazy."""
        self.id = None
        self.title = None
        self.description = None
        self.category_id = None
        self.language_id = None
        self.difficulty = 1
        self.xp_reward = 10
        self.order_index = None
        self.is_active = True
        super().__init__(data)
    
    @classmethod
    def get_by_language(cls, language_id):
        """Pobiera wszystkie lekcje dla danego języka."""
        with DatabaseManager() as db:
            data = db.fetch_all(
                "SELECT * FROM lessons WHERE language_id = ? AND is_active = 1 ORDER BY order_index",
                (language_id,)
            )
            return [cls(item) for item in data]
    
    @classmethod
    def get_by_category(cls, category_id):
        """Pobiera wszystkie lekcje dla danej kategorii."""
        with DatabaseManager() as db:
            data = db.fetch_all(
                "SELECT * FROM lessons WHERE category_id = ? AND is_active = 1 ORDER BY order_index",
                (category_id,)
            )
            return [cls(item) for item in data]
    
    def get_exercises(self):
        """Pobiera wszystkie ćwiczenia dla tej lekcji."""
        from database.models import Exercise
        return Exercise.get_by_lesson(self.id)
    
    def save(self):
        """Zapisuje lub aktualizuje lekcję w bazie danych."""
        with DatabaseManager() as db:
            if self.id:
                data = {
                    'title': self.title,
                    'description': self.description,
                    'category_id': self.category_id,
                    'language_id': self.language_id,
                    'difficulty': self.difficulty,
                    'xp_reward': self.xp_reward,
                    'order_index': self.order_index,
                    'is_active': self.is_active
                }
                db.update('lessons', data, 'id = ?', (self.id,))
                return self.id
            else:
                data = {
                    'title': self.title,
                    'description': self.description,
                    'category_id': self.category_id,
                    'language_id': self.language_id,
                    'difficulty': self.difficulty,
                    'xp_reward': self.xp_reward,
                    'order_index': self.order_index,
                    'is_active': self.is_active
                }
                self.id = db.insert('lessons', data)
                return self.id

class Exercise(BaseModel):
    """Model reprezentujący ćwiczenie w systemie."""
    
    table_name = "exercises"
    
    def __init__(self, data=None):
        """Inicjalizuje ćwiczenie z danych z bazy."""
        self.id = None
        self.lesson_id = None
        self.type = None
        self.content = None
        self.correct_answer = None
        self.options = None
        self.hint = None
        self.image_path = None
        self.audio_path = None
        self.xp_reward = 5
        self.order_index = None
        super().__init__(data)
    
    @classmethod
    def get_by_lesson(cls, lesson_id):
        """Pobiera wszystkie ćwiczenia dla danej lekcji."""
        with DatabaseManager() as db:
            data = db.fetch_all(
                "SELECT * FROM exercises WHERE lesson_id = ? ORDER BY order_index",
                (lesson_id,)
            )
            return [cls(item) for item in data]
    
    def save(self):
        """Zapisuje lub aktualizuje ćwiczenie w bazie danych."""
        with DatabaseManager() as db:
            if self.id:
                data = {
                    'lesson_id': self.lesson_id,
                    'type': self.type,
                    'content': self.content,
                    'correct_answer': self.correct_answer,
                    'options': self.options,
                    'hint': self.hint,
                    'image_path': self.image_path,
                    'audio_path': self.audio_path,
                    'xp_reward': self.xp_reward,
                    'order_index': self.order_index
                }
                db.update('exercises', data, 'id = ?', (self.id,))
                return self.id
            else:
                data = {
                    'lesson_id': self.lesson_id,
                    'type': self.type,
                    'content': self.content,
                    'correct_answer': self.correct_answer,
                    'options': self.options,
                    'hint': self.hint,
                    'image_path': self.image_path,
                    'audio_path': self.audio_path,
                    'xp_reward': self.xp_reward,
                    'order_index': self.order_index
                }
                self.id = db.insert('exercises', data)
                return self.id