from App import *

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
        # margine inferiore 30px: lascia spazio alla progress bar (26px) + 4px gap
        grid.setContentsMargins(24, 24, 24, 30)

        # Tutte e 3 le righe del grid si espandono equamente
        for r in range(3):
            grid.setRowStretch(r, 1)

        # Colonne distribuite equamente
        for c in range(3):
            grid.setColumnStretch(c, 1)

        # --- (0,0) Pulsante importazione ---
        self.btn_importa = QPushButton("📂  Importa Excel")
        apply_button_style(self.btn_importa, "primary")
        self.excel = MainExcel(self)
        self.btn_importa.clicked.connect(self.excel.start_import)
        grid.addWidget(self.btn_importa, 0, 0)

        # --- (0,1) Pulsante nuova importazione (abilitato solo a fine ciclo) ---
        self.btn_nuova = QPushButton("🔄  Nuova Importazione")
        apply_button_style(self.btn_nuova, "secondary")
        self.btn_nuova.setEnabled(False)
        self.btn_nuova.clicked.connect(self._nuova_importazione)
        grid.addWidget(self.btn_nuova, 0, 1)

        # --- (1,0) Pulsante Aggiorna Support Table ---
        self.btn_support = QPushButton("🔁  Aggiorna\nSupport Table")
        apply_button_style(self.btn_support, "warning")
        grid.addWidget(self.btn_support, 1, 0)

        # --- (1, 1:3) Label di stato ---
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background-color: transparent;")
        grid.addWidget(self.label, 1, 1, 1, 2)

        # --- (2,2) Pulsante torna alla finestra principale ---
        btn_indietro = QPushButton("🏠  Menu principale")
        apply_button_style(btn_indietro, "secondary")
        btn_indietro.clicked.connect(self._torna_al_menu)
        grid.addWidget(btn_indietro, 2, 2)

        self.setLayout(grid)

        # --- Barra di avanzamento: posizionata manualmente in resizeEvent ---
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(22)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 1px solid #555; border-radius: 4px;"
            " background: rgba(0,0,0,0.4); color: white; text-align: center; }"
            "QProgressBar::chunk { background: #4CAF50; border-radius: 3px; }"
        )

    # ------------------------------------------------------------------
    # Azioni pulsanti
    # ------------------------------------------------------------------
    def _nuova_importazione(self):
        """Resetta la UI e riabilita il pulsante principale per un nuovo ciclo."""
        self.btn_nuova.setEnabled(False)
        self.btn_importa.setEnabled(True)
        self.label.setText("")
        self.progress_bar.setValue(0)

    def _torna_al_menu(self):
        self.close()

    def closeEvent(self, event):
        """Ferma i thread attivi prima di chiudere per evitare 'QMutex: destroying locked mutex'."""
        self.excel.cleanup()
        super().closeEvent(event)

    # ------------------------------------------------------------------
    # Ridimensionamento sfondo (cover centrato)
    # ------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Sfondo cover centrato
        bg = self._bg_label
        if bg is not None:
            src = getattr(bg, "_src_pixmap", None)
            if src is not None:
                scaled = src.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = (self.width() - scaled.width()) // 2
                y = (self.height() - scaled.height()) // 2
                bg.setPixmap(scaled)
                bg.setGeometry(x, y, scaled.width(), scaled.height())
        # Progress bar sempre incollata al fondo (22px altezza + 2px sopra + 2px sotto)
        pb_h = 26
        self.progress_bar.setGeometry(
            24, self.height() - pb_h + 2, self.width() - 48, 22
        )
