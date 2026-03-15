from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from db.database import inserisci_utente, lista_utenti
from controllers.main_excel import MainExcel

# IMPORTA I MODULI DI STILE
from ui.style.background_style import apply_background
from ui.style.button_styles import apply_button_style


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestione Excel")
        self._bg_label = (
            None  # inizializzato prima di resize() che triggera resizeEvent
        )
        self.resize(800, 600)

        # SFONDO PERSONALIZZATO
        self._bg_label = apply_background(
            self, "assets/backgrounds/wallpaper_dl.png", opacity=0.35
        )

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Benvenuto nella tua app PySide6!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_label = QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: white; background-color: transparent;")

        # Pulsanti
        button_db = QPushButton("Salva utente")
        apply_button_style(button_db, "primary")
        button_db.clicked.connect(self.on_click)

        button_excel = QPushButton("Importa Excel")
        apply_button_style(button_excel, "primary")

        # Collegamento al controller Excel
        self.excel = MainExcel(self)
        button_excel.clicked.connect(self.excel.start_import)

        layout.addWidget(self.label)
        layout.addWidget(button_db)
        layout.addWidget(button_excel)

        self.setLayout(layout)

    def resizeEvent(self, event):
        """Ridimensiona lo sfondo mantenendo il fattore di forma (cover centrato)."""
        super().resizeEvent(event)
        bg = self._bg_label
        if bg is None:
            return
        src: object = getattr(bg, "_src_pixmap", None)
        if src is None:
            return
        scaled = src.scaled(  # type: ignore[union-attr]
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        # Centra la label in modo che l'immagine copra tutta la finestra
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        bg.setPixmap(scaled)
        bg.setGeometry(x, y, scaled.width(), scaled.height())

    def on_click(self):
        inserisci_utente("Roberto")
        utenti = lista_utenti()
        self.label.setText(f"Utenti salvati nel DB: {len(utenti)}")
