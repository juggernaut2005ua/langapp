# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

def set_application_style(app):
    """Ustawia globalny styl aplikacji."""
    # Ustawianie niestandardowej palety kolorów
    palette = QPalette()
    
    # Grupa kolorów dla aplikacji
    primary_color = QColor(52, 152, 219)    # niebieski
    secondary_color = QColor(41, 128, 185)   # ciemniejszy niebieski
    accent_color = QColor(46, 204, 113)      # zielony
    background_color = QColor(236, 240, 241) # jasny szary
    text_color = QColor(44, 62, 80)          # ciemny granatowy
    error_color = QColor(231, 76, 60)        # czerwony
    
    # Ustawienie kolorów dla różnych elementów interfejsu
    palette.setColor(QPalette.Window, background_color)
    palette.setColor(QPalette.WindowText, text_color)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, background_color)
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, text_color)
    palette.setColor(QPalette.Text, text_color)
    palette.setColor(QPalette.Button, primary_color)
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, secondary_color)
    palette.setColor(QPalette.Highlight, accent_color)
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Ustawienie palety dla aplikacji
    app.setPalette(palette)
    
    # Ustawienie czcionki dla całej aplikacji
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Definicja stylu CSS dla różnych elementów interfejsu
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        
        QLabel {
            color: #2c3e50;
        }
        
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
        }
        
        QLabel#errorLabel {
            color: #e74c3c;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1f6dad;
        }
        
        QPushButton#successButton {
            background-color: #2ecc71;
        }
        
        QPushButton#successButton:hover {
            background-color: #27ae60;
        }
        
        QPushButton#successButton:pressed {
            background-color: #1e8449;
        }
        
        QPushButton#dangerButton {
            background-color: #e74c3c;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #c0392b;
        }
        
        QPushButton#dangerButton:pressed {
            background-color: #a33025;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
            color: #2c3e50;
        }
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #3498db;
        }
        
        QGroupBox {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            margin-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #2c3e50;
        }
        
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
        }
        
        QTabBar::tab {
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: none;
        }
        
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
        
        QProgressBar {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            text-align: center;
            color: white;
            background-color: #ecf0f1;
        }
        
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 3px;
        }
        
        QMenuBar {
            background-color: #3498db;
            color: white;
        }
        
        QMenuBar::item {
            padding: 8px 16px;
            background: transparent;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #2980b9;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #bdc3c7;
        }
        
        QMenu::item {
            padding: 6px 24px 6px 16px;
        }
        
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #ecf0f1;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #bdc3c7;
            min-height: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QScrollBar:horizontal {
            border: none;
            background: #ecf0f1;
            height: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background: #bdc3c7;
            min-width: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
    """)

    return app