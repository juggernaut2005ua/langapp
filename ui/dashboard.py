# -*- coding: utf-8 -*-

import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QMessageBox, QTabWidget,
                            QGridLayout, QProgressBar, QGroupBox, QScrollArea,
                            QSizePolicy, QStackedWidget, QFrame)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from auth.login_manager import LoginManager
from database.models import Language, Lesson, User
from ui.lesson_browser import LessonBrowserWidget
from ui.profile_view import ProfileWidget
from config import APP_NAME, LOGO_PATH

logger = logging.getLogger(__name__)

class DashboardWindow(QMainWindow):
    """Główne okno z dashboardem użytkownika po zalogowaniu."""
    
    def __init__(self):
        super().__init__()
        self.user = LoginManager.get_current_user()
        if not self.user:
            # Jeśli z jakiegoś powodu nie ma użytkownika, zamykamy okno
            logger.error("Próba otwarcia dashboardu bez zalogowanego użytkownika")
            self.close()
            return
        
        self.setWindowTitle(f"{APP_NAME} - Dashboard")
        self.setMinimumSize(900, 700)
        self.setup_ui()
        self.load_user_data()
    
    def setup_ui(self):
        """Konfiguruje interfejs użytkownika."""
        # Widget centralny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        
        # Pasek górny z logo i informacjami o użytkowniku
        top_bar = QHBoxLayout()
        
        # Logo aplikacji
        logo_label = QLabel()
        logo_pixmap = QPixmap(LOGO_PATH)
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaledToHeight(40, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        top_bar.addWidget(logo_label)
        
        # Tytuł aplikacji
        title_label = QLabel(APP_NAME)
        title_label.setObjectName("titleLabel")
        top_bar.addWidget(title_label)
        
        top_bar.addStretch()
        
        # Informacje o użytkowniku
        user_info = QLabel(f"Zalogowany jako: {self.user.username}")
        top_bar.addWidget(user_info)
        
        # Przycisk wylogowania
        logout_button = QPushButton("Wyloguj")
        logout_button.clicked.connect(self.handle_logout)
        top_bar.addWidget(logout_button)
        
        main_layout.addLayout(top_bar)
        
        # Widok z zakładkami
        self.tab_widget = QTabWidget()
        
        # Zakładka Dashboard
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_tab)
        
        # Przywitanie użytkownika
        welcome_label = QLabel(f"Witaj, {self.user.username}!")
        welcome_label.setObjectName("titleLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(welcome_label)
        
        # Widget z postępami
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        
        progress_title = QLabel("Twoje postępy")
        progress_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        progress_layout.addWidget(progress_title)
        
        # Panel z językami
        self.languages_grid = QGridLayout()
        self.languages_grid.setSpacing(20)
        progress_layout.addLayout(self.languages_grid)
        
        # Statystyki
        stats_group = QGroupBox("Statystyki")
        stats_layout = QGridLayout(stats_group)
        
        self.xp_label = QLabel("Łączne doświadczenie: 0 XP")
        stats_layout.addWidget(self.xp_label, 0, 0)
        
        self.lessons_completed_label = QLabel("Ukończone lekcje: 0")
        stats_layout.addWidget(self.lessons_completed_label, 0, 1)
        
        self.streak_label = QLabel("Aktualny streak: 0 dni")
        stats_layout.addWidget(self.streak_label, 1, 0)
        
        self.exercises_completed_label = QLabel("Ukończone ćwiczenia: 0")
        stats_layout.addWidget(self.exercises_completed_label, 1, 1)
        
        progress_layout.addWidget(stats_group)
        
        # Osiągnięcia
        achievements_group = QGroupBox("Ostatnie osiągnięcia")
        achievements_layout = QVBoxLayout(achievements_group)
        
        self.achievements_label = QLabel("Nie masz jeszcze żadnych osiągnięć.")
        achievements_layout.addWidget(self.achievements_label)
        
        progress_layout.addWidget(achievements_group)
        
        # Dodanie widgetu z postępami do głównego layoutu
        dashboard_layout.addWidget(progress_widget)
        
        # Przyciski szybkiego dostępu
        quick_access_layout = QHBoxLayout()
        
        start_learning_button = QPushButton("Rozpocznij naukę")
        start_learning_button.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        quick_access_layout.addWidget(start_learning_button)
        
        view_profile_button = QPushButton("Twój profil")
        view_profile_button.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        quick_access_layout.addWidget(view_profile_button)
        
        if self.user.is_admin:
            admin_panel_button = QPushButton("Panel administratora")
            admin_panel_button.clicked.connect(self.open_admin_panel)
            quick_access_layout.addWidget(admin_panel_button)
        
        dashboard_layout.addLayout(quick_access_layout)
        
        # Dodanie zakładki Dashboard do widoku z zakładkami
        self.tab_widget.addTab(dashboard_tab, "Dashboard")
        
        # Zakładka z lekcjami
        self.lesson_browser = LessonBrowserWidget()
        self.tab_widget.addTab(self.lesson_browser, "Lekcje")
        
        # Zakładka z profilem
        self.profile_widget = ProfileWidget(self.user)
        self.tab_widget.addTab(self.profile_widget, "Profil")
        
        # Dodanie widoku z zakładkami do głównego layoutu
        main_layout.addWidget(self.tab_widget)
    
    def load_user_data(self):
        """Wczytuje dane użytkownika i aktualizuje UI."""
        # Pobieranie języków
        languages = Language.get_active()
        
        # Tworzenie kart dla każdego języka
        for i, language in enumerate(languages):
            row, col = divmod(i, 3)
            
            # Tworzenie ramki dla języka
            language_frame = QFrame()
            language_frame.setFrameShape(QFrame.StyledPanel)
            language_frame.setMinimumHeight(120)
            language_frame.setMinimumWidth(250)
            
            language_layout = QVBoxLayout(language_frame)
            
            # Nazwa języka
            language_name = QLabel(language.name)
            language_name.setFont(QFont("Segoe UI", 12, QFont.Bold))
            language_layout.addWidget(language_name)
            
            # Postęp w nauce
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)  # W rzeczywistej aplikacji trzeba będzie obliczać postęp
            language_layout.addWidget(progress_bar)
            
            # Przycisk do nauki
            learn_button = QPushButton(f"Ucz się {language.name}")
            learn_button.clicked.connect(lambda checked, lang=language: self.start_learning(lang))
            language_layout.addWidget(learn_button)
            
            self.languages_grid.addWidget(language_frame, row, col)
        
        # Aktualizacja statystyk
        stats = self.user.get_stats()
        if stats:
            self.xp_label.setText(f"Łączne doświadczenie: {stats['total_xp']} XP")
            self.lessons_completed_label.setText(f"Ukończone lekcje: {stats['lessons_completed']}")
            self.exercises_completed_label.setText(f"Ukończone ćwiczenia: {stats['exercises_completed']}")
        
        # Aktualizacja streaka
        streak_info = self.user.get_streak()
        if streak_info:
            self.streak_label.setText(f"Aktualny streak: {streak_info['current_streak']} dni")
    
    def start_learning(self, language):
        """Rozpoczyna naukę wybranego języka."""
        self.tab_widget.setCurrentIndex(1)
        self.lesson_browser.select_language(language.id)
    
    def handle_logout(self):
        """Obsługuje wylogowanie użytkownika."""
        reply = QMessageBox.question(
            self,
            "Wylogowanie",
            "Czy na pewno chcesz się wylogować?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            LoginManager.logout()
            
            # Otwarcie okna logowania
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            
            # Zamknięcie dashboardu
            self.close()
    
    def open_admin_panel(self):
        """Otwiera panel administratora."""
        if not self.user.is_admin:
            QMessageBox.warning(
                self,
                "Brak uprawnień",
                "Nie masz uprawnień administratora."
            )
            return
        
        from ui.admin_panel import AdminPanelWindow
        self.admin_panel = AdminPanelWindow()
        self.admin_panel.show()