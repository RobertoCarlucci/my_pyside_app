from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

from db.database import init_db, inserisci_utente, lista_utenti
from excel.excel_loader import carica_excel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Inizializza il database
        init_db()

        # Imposta dimensione iniziale della finestra
        self.resize(600, 400)
        self.setWindowTitle("Template PySide6 + SQLite + Excel")

        # Sfondo verde chiaro
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ccffcc"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout principale
        layout = QVBoxLayout()

        # Label centrata, corpo 12, bold, rossa
        self.label = QLabel("Benvenuto nella tua app PySide6!")
        self.label.setAlignment(Qt.AlignCenter)

        font_label = QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: red;")

        # Pulsante: salva utente nel DB
        button_db = QPushButton("Salva utente")
        font_button = QFont()
        font_button.setPointSize(12)
        font_button.setBold(True)
        button_db.setFont(font_button)

        button_db.setStyleSheet(
            """
            QPushButton {
                background-color: yellow;
                color: fuchsia;
                border: 2px solid #555;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #fff799;
            }
        """
        )

        button_db.clicked.connect(self.on_click)

        # Pulsante: importa Excel
        button_excel = QPushButton("Importa Excel")
        button_excel.setFont(font_button)
        button_excel.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border: 2px solid #555;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #d6ecff;
            }
        """
        )

        button_excel.clicked.connect(self.importa_excel)

        # Aggiunta widget al layout
        layout.addWidget(self.label)
        layout.addWidget(button_db)
        layout.addWidget(button_excel)

        self.setLayout(layout)

    # --- EVENTI ---

    def on_click(self):
        """Salva un utente fittizio nel DB e aggiorna la label."""
        inserisci_utente("Roberto")
        utenti = lista_utenti()
        self.label.setText(f"Utenti salvati nel DB: {len(utenti)}")

    def importa_excel(self):
        """Apre un file Excel e mostra quante righe contiene."""
        file_path
