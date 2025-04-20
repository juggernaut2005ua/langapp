# -*- coding: utf-8 -*-

import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QFormLayout, QGroupBox, QTabWidget, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from auth.user_manager import UserManager
from auth.login_manager import LoginManager
from ui.main_window import MainWindow
from ui.dashboard import DashboardWindow
from config import APP_NAME, LOGO_PATH

logger = logging.getLogger(__name__)

class LoginWindow(QMainWindow):
    """Okno logowania i rejestracji użytkownika."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - Logowanie")
        self.setMinimumSize(450, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """Konfiguruje interfejs użytkownika."""
        # Widget centralny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)
        
        # Logo aplikacji
        logo_label = QLabel()
        logo_pixmap = QPixmap(LOGO_PATH)
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaledToWidth(150, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(logo_label)
        
        # Tytuł aplikacji
        title_label = QLabel(APP_NAME)
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Widget z zakładkami
        tab_widget = QTabWidget()
        login_tab = QWidget()
        register_tab = QWidget()
        tab_widget.addTab(login_tab, "Logowanie")
        tab_widget.addTab(register_tab, "Rejestracja")
        main_layout.addWidget(tab_widget)
        
        # Formularz logowania
        login_layout = QVBoxLayout(login_tab)
        login_layout.setSpacing(15)
        
        login_form = QFormLayout()
        login_form.setSpacing(10)
        login_form.setLabelAlignment(Qt.AlignRight)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Podaj nazwę użytkownika")
        login_form.addRow("Nazwa użytkownika:", self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Podaj hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        login_form.addRow("Hasło:", self.password_input)
        
        self.remember_checkbox = QCheckBox("Zapamiętaj mnie")
        login_form.addRow("", self.remember_checkbox)
        
        login_layout.addLayout(login_form)
        
        self.login_error_label = QLabel()
        self.login_error_label.setObjectName("errorLabel")
        self.login_error_label.setAlignment(Qt.AlignCenter)
        self.login_error_label.setVisible(False)
        login_layout.addWidget(self.login_error_label)
        
        # Przycisk logowania
        login_button = QPushButton("Zaloguj się")
        login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(login_button)
        
        # Formularz rejestracji
        register_layout = QVBoxLayout(register_tab)
        register_layout.setSpacing(15)
        
        register_form = QFormLayout()
        register_form.setSpacing(10)
        register_form.setLabelAlignment(Qt.AlignRight)
        
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Wybierz nazwę użytkownika")
        register_form.addRow("Nazwa użytkownika:", self.reg_username_input)
        
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Podaj adres email")
        register_form.addRow("Email:", self.reg_email_input)
        
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Minimum 8 znaków, wielkie litery, cyfry")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        register_form.addRow("Hasło:", self.reg_password_input)
        
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("Powtórz hasło")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        register_form.addRow("Powtórz hasło:", self.reg_confirm_password_input)
        
        register_layout.addLayout(register_form)
        
        self.register_error_label = QLabel()
        self.register_error_label.setObjectName("errorLabel")
        self.register_error_label.setAlignment(Qt.AlignCenter)
        self.register_error_label.setVisible(False)
        register_layout.addWidget(self.register_error_label)
        
        # Przycisk rejestracji
        register_button = QPushButton("Zarejestruj się")
        register_button.clicked.connect(self.handle_register)
        register_layout.addWidget(register_button)
        
        # Przycisk do testowania aplikacji bez logowania (tylko w fazie rozwoju)
        debug_login_button = QPushButton("Debuguj bez logowania")
        debug_login_button.clicked.connect(self.debug_login)
        main_layout.addWidget(debug_login_button)
    
    def handle_login(self):
        """Obsługuje proces logowania."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.login_error_label.setText("Proszę wypełnić wszystkie pola")
            self.login_error_label.setVisible(True)
            return
        
        # Autentykacja użytkownika
        user, error = UserManager.authenticate_user(username, password)
        
        if user:
            # Zapisanie informacji o zalogowanym użytkowniku
            LoginManager.login(user)
            
            # Otwarcie głównego okna aplikacji
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            
            # Zamknięcie okna logowania
            self.close()
        else:
            self.login_error_label.setText(error)
            self.login_error_label.setVisible(True)
    
    def handle_register(self):
        """Obsługuje proces rejestracji."""
        username = self.reg_username_input.text().strip()
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        
        # Walidacja pól
        if not username or not email or not password or not confirm_password:
            self.register_error_label.setText("Proszę wypełnić wszystkie pola")
            self.register_error_label.setVisible(True)
            return
        
        if password != confirm_password:
            self.register_error_label.setText("Hasła nie są identyczne")
            self.register_error_label.setVisible(True)
            return
        
        # Rejestracja użytkownika
        user, error = UserManager.register_user(username, email, password)
        
        if user:
            # Wyświetlenie informacji o sukcesie
            QMessageBox.information(
                self,
                "Rejestracja udana",
                f"Konto dla użytkownika {username} zostało utworzone. Możesz się teraz zalogować."
            )
            
            # Przełączenie na zakładkę logowania
            self.reg_username_input.clear()
            self.reg_email_input.clear()
            self.reg_password_input.clear()
            self.reg_confirm_password_input.clear()
            self.register_error_label.setVisible(False)
            
            tab_widget = self.centralWidget().findChild(QTabWidget)
            tab_widget.setCurrentIndex(0)
        else:
            self.register_error_label.setText(error)
            self.register_error_label.setVisible(True)
    
    def debug_login(self):
        """Funkcja do testowania - loguje jako administrator bez weryfikacji hasła."""
        from database.models import User
        admin_user = User.get_by_username("admin")
        
        if admin_user:
            LoginManager.login(admin_user)
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Błąd debugowania",
                "Nie znaleziono administratora. Upewnij się, że baza danych została zainicjalizowana."
            )