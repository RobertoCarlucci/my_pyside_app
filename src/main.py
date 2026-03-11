import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

from db.database import init_db, inserisci_utente, lista_utenti
from excel.file_selector import FileSelector
from excel.file_authorizer import FileAuthorizer
from excel.file_model import FileModel
from excel.excel_loader import carica_excel
from excel.excel_validator import ExcelValidator


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
        palette.setColor(QPalette.ColorRole.Window, QColor("#ccffcc"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout principale
        layout = QVBoxLayout()

        # Label centrata, corpo 12, bold, rossa
        self.label = QLabel("Benvenuto nella tua app PySide6!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_label = QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: red;")

        # Font comune per i pulsanti
        font_button = QFont()
        font_button.setPointSize(12)
        font_button.setBold(True)

        # Pulsante: salva utente nel DB
        button_db = QPushButton("Salva utente")
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
        """Gestisce l'intero flusso di importazione Excel."""

        # 1. Selezione file
        file_path = FileSelector.seleziona_excel(self)
        if not file_path:
            return

        # 1. Ottieni il codice del file (es. "res10")
        codice = FileAuthorizer.get_codice(file_path)
        if codice is None:
            self.label.setText("❌ File non autorizzato")
            return

        # 2. Carica Excel
        df = carica_excel(file_path)
        if df is None:
            self.label.setText("❌ Errore nel caricamento Excel")
            return

        # 3. Ottieni le colonne attese dal modello JSON
        colonne_attese = FileModel.get_colonne_attese(codice)
        if not colonne_attese:
            self.label.setText("❌ Modello colonne non trovato")
            return

        # 4. Valida e mappa le colonne
        ok, df_validato, errori = ExcelValidator.valida(df, colonne_attese)

        if not ok:
            self.label.setText("❌ Errori nella struttura del file")
            print(errori)  # utile per debug
            return

        # 5. Import riuscito
        self.label.setText(f"✔️ File {codice} importato correttamente")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
