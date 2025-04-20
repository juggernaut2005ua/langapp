# -*- coding: utf-8 -*-

import sqlite3
import logging
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Klasa zarządzająca połączeniem z bazą danych SQLite."""
    
    def __init__(self, db_path=DATABASE_PATH):
        """Inicjalizacja managera bazy danych."""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Ustanawia połączenie z bazą danych."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            # Włączenie obsługi kluczy obcych
            self.connection.execute("PRAGMA foreign_keys = ON")
            # Ustawienie zwracania wierszy jako słowniki
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.debug(f"Połączono z bazą danych: {self.db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas łączenia z bazą danych: {e}")
            return False
    
    def disconnect(self):
        """Zamyka połączenie z bazą danych."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            logger.debug("Zamknięto połączenie z bazą danych")
    
    def execute_query(self, query, params=None):
        """Wykonuje zapytanie SQL bez zwracania wyników."""
        if not self.connection:
            self.connect()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Błąd wykonania zapytania: {e}\nZapytanie: {query}\nParametry: {params}")
            return False
    
    def fetch_one(self, query, params=None):
        """Wykonuje zapytanie i zwraca jeden wynik."""
        if not self.connection:
            self.connect()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas pobierania wiersza: {e}\nZapytanie: {query}\nParametry: {params}")
            return None
    
    def fetch_all(self, query, params=None):
        """Wykonuje zapytanie i zwraca wszystkie wyniki jako listę słowników."""
        if not self.connection:
            self.connect()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            return [dict(row) for row in results] if results else []
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas pobierania wierszy: {e}\nZapytanie: {query}\nParametry: {params}")
            return []
    
    def insert(self, table, data):
        """Wstawia dane do tabeli i zwraca ID wstawionego wiersza."""
        if not self.connection:
            self.connect()
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas wstawiania danych: {e}\nTabela: {table}\nDane: {data}")
            return None
    
    def update(self, table, data, condition, condition_params):
        """Aktualizuje dane w tabeli według określonego warunku."""
        if not self.connection:
            self.connect()
        
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        values = tuple(data.values()) + condition_params
        
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas aktualizacji danych: {e}\nTabela: {table}\nDane: {data}\nWarunek: {condition}")
            return 0
    
    def delete(self, table, condition, params):
        """Usuwa dane z tabeli według określonego warunku."""
        if not self.connection:
            self.connect()
        
        query = f"DELETE FROM {table} WHERE {condition}"
        
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Błąd podczas usuwania danych: {e}\nTabela: {table}\nWarunek: {condition}")
            return 0
    
    def __enter__(self):
        """Pozwala na używanie managera w bloku 'with'."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Zamyka połączenie po wyjściu z bloku 'with'."""
        self.disconnect()