from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

from db.database import init_db, inserisci_utente, lista_utenti
from controllers.main_excel import MainExcel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        init_db()
        self.setWindowTitle("Gestione Excel")
        self.resize(600, 400)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ccffcc"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Benvenuto!")
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # Pulsante DB
        btn_db = QPushButton("Salva utente")
        btn_db.clicked.connect(self.salva_utente)
        layout.addWidget(btn_db)

        # Pulsante Excel
        btn_excel = QPushButton("Importa Excel")
        layout.addWidget(btn_excel)

        # Controller Excel
        self.excel = MainExcel(self)
        btn_excel.clicked.connect(self.excel.start_import)

        self.setLayout(layout)

    def salva_utente(self):
        inserisci_utente("Roberto")
        utenti = lista_utenti()
        self.label.setText(f"Utenti salvati: {len(utenti)}")
