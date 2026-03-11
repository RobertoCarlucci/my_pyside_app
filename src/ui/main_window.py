from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

from db.database import init_db, inserisci_utente, lista_utenti
from controllers.main_excel import MainExcel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        init_db()

        self.resize(600, 400)
        self.setWindowTitle("Template PySide6 + SQLite + Excel")

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ccffcc"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Benvenuto nella tua app PySide6!")
        self.label.setAlignment(Qt.AlignCenter)

        font_label = QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: red;")

        # Pulsanti
        font_button = QFont()
        font_button.setPointSize(12)
        font_button.setBold(True)

        button_db = QPushButton("Salva utente")
        button_db.setFont(font_button)
        button_db.clicked.connect(self.on_click)

        button_excel = QPushButton("Importa Excel")
        button_excel.setFont(font_button)

        # Collegamento al controller Excel
        self.excel = MainExcel(self)
        button_excel.clicked.connect(self.excel.start_import)

        layout.addWidget(self.label)
        layout.addWidget(button_db)
        layout.addWidget(button_excel)

        self.setLayout(layout)

    def on_click(self):
        inserisci_utente("Roberto")
        utenti = lista_utenti()
        self.label.setText(f"Utenti salvati nel DB: {len(utenti)}")
