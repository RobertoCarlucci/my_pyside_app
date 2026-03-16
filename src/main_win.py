from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PySide6.QtCore import Qt

from db.database import init_db, crea_tabelle_modelli
from excel.file_model import FileModel
from ui.style.background_style import apply_background
from ui.style.button_styles import apply_button_style


class MainWindow(QWidget):
    """
    Finestra principale hub dell'applicazione.
    Layout: griglia 3 colonne × 3 righe
      (0,0) → Gestione Excel  (apre ExcelWindow)
      (2,2) → Esci
    """

    def __init__(self):
        super().__init__()

        # Inizializzazione DB e tabelle modelli
        init_db()
        modelli = []
        for codice in FileModel.get_all_models():
            try:
                m = FileModel.load_model(codice)
                if m:
                    modelli.append(m)
            except ValueError as e:
                QMessageBox.warning(
                    self,
                    "Modello non valido",
                    f"Il file {codice}.json contiene errori e verrà ignorato:\n\n{e}",
                )
        crea_tabelle_modelli(modelli)

        self.setWindowTitle("Gestione")
        self._bg_label = None
        self.resize(900, 650)

        # Sfondo personalizzato
        self._bg_label = apply_background(
            self, "assets/backgrounds/wallpaper_dl.png", opacity=0.35
        )

        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(40, 40, 40, 40)

        for r in range(3):
            grid.setRowStretch(r, 1)
        for c in range(3):
            grid.setColumnStretch(c, 1)

        # --- (0,0) Gestione Excel ---
        btn_excel = QPushButton("📊  Gestione Excel")
        apply_button_style(btn_excel, "primary")
        btn_excel.clicked.connect(self._apri_excel_window)
        grid.addWidget(btn_excel, 0, 0)

        # --- (2,2) Esci ---
        btn_esci = QPushButton("🚪  Esci")
        apply_button_style(btn_esci, "danger")
        btn_esci.clicked.connect(self._esci)
        grid.addWidget(btn_esci, 2, 2)

        self.setLayout(grid)

        # Riferimento alla finestra Excel (lazy, creata al primo click)
        self._excel_window = None

    # ------------------------------------------------------------------
    # Azioni pulsanti
    # ------------------------------------------------------------------
    def _apri_excel_window(self):
        from ui.excel_window import ExcelWindow

        if self._excel_window is None:
            self._excel_window = ExcelWindow()
        self._excel_window.show()
        self._excel_window.raise_()
        self._excel_window.activateWindow()

    def _esci(self):
        risposta = QMessageBox.question(
            self,
            "Conferma uscita",
            "Sei sicuro di voler uscire?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if risposta == QMessageBox.StandardButton.Yes:
            QApplication.quit()

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
