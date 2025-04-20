# -*- coding: utf-8 -*-

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                           QComboBox, QScrollArea, QGridLayout, QGroupBox, QFrame,
                           QSizePolicy, QProgressBar, QStackedWidget)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from database.models import Language, Lesson
from ui.exercise_view import ExerciseView

logger = logging.getLogger(__name__)

class LessonBrowserWidget(QWidget):
    """Widget do przeglądania i wyboru lekcji."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_language_id = None
        self.setup_ui()
        self.load_languages()
    
    def setup_ui(self):
        """Konfiguruje interfejs użytkownika."""
        main_layout = QVBoxLayout(self)
        
        # Górny panel z wyborem języka
        top_panel = QHBoxLayout()
        
        language_label = QLabel("Wybierz język:")
        top_panel.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.currentIndexChanged.connect(self.language_changed)
        top_panel.addWidget(self.language_combo)
        
        top_panel.addStretch()
        
        main_layout.addLayout(top_panel)
        
        # Obszar z lekcjami
        self.lesson_area_stack = QStackedWidget()
        
        # Widok pustego ekranu
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_message = QLabel("Wybierz język, aby zobaczyć dostępne lekcje")
        empty_message.setFont(QFont("Segoe UI", 16))
        empty_message.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_message)
        
        self.lesson_area_stack.addWidget(empty_widget)
        
        # Widok lekcji
        self.lessons_widget = QWidget()
        lessons_layout = QVBoxLayout(self.lessons_widget)
        
        # Tytuł sekcji lekcji
        self.lessons_title = QLabel("Lekcje")
        self.lessons_title.setFont(QFont("Segoe UI", 14, QFont.Bold))