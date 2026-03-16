from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QProgressBar,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from controllers.main_excel import MainExcel
from ui.style.background_style import apply_background
from ui.style.button_styles import apply_button_style


class ExcelWindow(QWidget):
    """
    Finestra di gestione importazione Excel.
    Layout: griglia 3 colonne × 4 righe
      (0,0)       → Pulsante "Importa Excel"
      (1, 0:3)    → Label di stato (span 3 colonne)
      (2, 0:3)    → Riga vuota (riservata a funzionalità future)
      (3, 0:3)    → Barra di avanzamento (span 3 colonne)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Gestione Excel")
        self._bg_label = None
        self.resize(800, 600)

        # Sfondo personalizzato
        self._bg_label = apply_background(
            self, "assets/backgrounds/wallpaper_dl.png", opacity=0.35
        )

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setContentsMargins(24, 24, 24, 24)

        # Righe 0-2 si espandono; riga 3 (progress) rimane compatta
        for r in range(3):
            grid.setRowStretch(r, 1)
        grid.setRowStretch(3, 0)

        # Colonne distribuite equamente
        for c in range(3):
            grid.setColumnStretch(c, 1)

        # --- (0,0) Pulsante importazione ---
        self.btn_importa = QPushButton("📂  Importa Excel")
        apply_button_style(self.btn_importa, "primary")
        self.excel = MainExcel(self)
        self.btn_importa.clicked.connect(self.excel.start_import)
        grid.addWidget(self.btn_importa, 0, 0)

        # --- (1, 0:3) Label di stato ---
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background-color: transparent;")
        grid.addWidget(self.label, 1, 0, 1, 3)

        # --- (3, 0:3) Barra di avanzamento ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 1px solid #555; border-radius: 4px;"
            " background: rgba(0,0,0,0.4); color: white; text-align: center; }"
            "QProgressBar::chunk { background: #4CAF50; border-radius: 3px; }"
        )
        grid.addWidget(self.progress_bar, 3, 0, 1, 3)

        # --- (2,2) Pulsante torna alla finestra principale ---
        btn_indietro = QPushButton("🏠  Menu principale")
        apply_button_style(btn_indietro, "secondary")
        btn_indietro.clicked.connect(self._torna_al_menu)
        grid.addWidget(btn_indietro, 2, 2)

        self.setLayout(grid)

    # ------------------------------------------------------------------
    # Azioni pulsanti
    # ------------------------------------------------------------------
    def _torna_al_menu(self):
        self.close()

    # ------------------------------------------------------------------
    # Ridimensionamento sfondo (cover centrato)
    # ------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        bg = self._bg_label
        if bg is None:
            return
        src = getattr(bg, "_src_pixmap", None)
        if src is None:
            return
        scaled = src.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        bg.setPixmap(scaled)
        bg.setGeometry(x, y, scaled.width(), scaled.height())
