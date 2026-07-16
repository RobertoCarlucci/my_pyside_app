import os

from PySide6.QtWidgets import QGridLayout, QPushButton, QMessageBox, QApplication, QFileDialog
from PySide6.QtCore import QSize

from db.database import init_db, crea_tabelle_modelli
from excel.excel_model import FileModel
from ui.style.button_styles import apply_button_style, get_icon
from ui.style.page_style import BasePage


class MainWindow(BasePage):
    """
    Finestra principale hub dell'applicazione.
    Layout: griglia 3 colonne × 3 righe
      (0,0) → Gestione Excel  (apre ExcelWindow)
      (2,2) → Esci
    """

    def __init__(self):
        super().__init__("Gestione Pv_PMO.")

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

        grid = QGridLayout(self.content)
        grid.setSpacing(16)
        grid.setContentsMargins(40, 40, 40, 40)

        for r in range(3):
            grid.setRowStretch(r, 1)
        for c in range(3):
            grid.setColumnStretch(c, 1)

        # --- (0,0) Conta Timesheet e invia mail resorce manager ---
        btn_excel = QPushButton("Crea mail Resorce Manager")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(self._carica_res10)
        grid.addWidget(btn_excel, 0, 0)

        # --- (0,1) Import Support Tables ---
        btn_excel = QPushButton("Import Support Tables")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(lambda: self._importa_gruppo("SupportTables"))
        grid.addWidget(btn_excel, 0, 1)

        # --- (1,1) Import Scenario Tables ---
        btn_excel = QPushButton("Import Scenario Tables")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(lambda: self._importa_gruppo("Scenario"))
        grid.addWidget(btn_excel, 1, 1)

        # --- (1,0) Import File Update Mensile PvPMO ---
        btn_excel = QPushButton("Import File Update Mensile PvPMO")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(lambda: self._importa_gruppo("UpdtPvPmo"))
        grid.addWidget(btn_excel, 0, 2)

        # --- (1,2) Set Date Update Mensile PvPMO ---
        btn_excel = QPushButton("Set Date Update Mensile PvPMO")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(self._apri_excel_window)
        grid.addWidget(btn_excel, 1, 2)

        # --- (2,2) Avvio Update Mensile PvPMO ---
        btn_excel = QPushButton("Avvio Update Mensile PvPMO")
        btn_excel.setIcon(get_icon("table-excel.png"))
        btn_excel.setIconSize(QSize(16, 16))
        apply_button_style(btn_excel, "my_button")
        btn_excel.clicked.connect(self._apri_excel_window)
        grid.addWidget(btn_excel, 2, 2)

        # --- (2,0) Esci ---
        btn_esci = QPushButton(" Esci")
        btn_esci.setIcon(get_icon("door-open-out.png"))
        btn_esci.setIconSize(QSize(16, 16))
        apply_button_style(btn_esci, "danger")
        btn_esci.clicked.connect(self._esci)
        grid.addWidget(btn_esci, 2, 0)

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

    def _carica_res10(self):
        from excel.excel_model import FileModel
        from excel.excel_loader import carica_excel
        from excel.excel_validator import ExcelValidator
        from excel.excel_importer import ExcelImporter
        from excel.excel_logger import ExcelLogger
        from ges_error.error_reporter import ErrorReporter
        from ui.preview_excel import PreviewExcel
        from ui.error_dialog import ErrorDialog
        from ui.warning_dialog import WarningDialog
        from PySide6.QtWidgets import QDialog

        modello = FileModel.load_model("res10")
        if not modello:
            QMessageBox.critical(self, "Errore", "Modello res10.json non trovato.")
            return

        nome_file_atteso = modello.get("nome_file", "RES10.xlsx")
        codice = modello.get("codice", "res10")

        cartella = QFileDialog.getExistingDirectory(
            self, "Seleziona la cartella contenente il file RES10"
        )
        if not cartella:
            return

        percorso_file = os.path.join(cartella, nome_file_atteso)
        if not os.path.isfile(percorso_file):
            reporter = ErrorReporter()
            reporter.add(f"Il file '{nome_file_atteso}' non è presente nella cartella selezionata.")
            ErrorDialog(reporter.get_error_text()).exec()
            return

        df = carica_excel(percorso_file)
        if df is None:
            reporter = ErrorReporter()
            reporter.add(f"Impossibile leggere il file '{nome_file_atteso}'.")
            ErrorDialog(reporter.get_error_text()).exec()
            return

        colonne_attese = modello.get("colonne_attese", [])
        tipi_attesi = modello.get("tipi_colonne", None)
        ok, df_validato, errori, warning = ExcelValidator.valida(df, colonne_attese, tipi_attesi)

        if not ok:
            reporter = ErrorReporter()
            reporter.extend_errors(errori)
            ErrorDialog(reporter.get_error_text()).exec()
            return

        if warning:
            reporter = ErrorReporter()
            reporter.extend_warnings(warning)
            dlg = WarningDialog(reporter.get_warning_text())
            if dlg.exec() == QDialog.DialogCode.Rejected:
                return

        def conferma_import():
            ExcelImporter.importa(codice, df_validato)
            evento = ExcelLogger.crea_evento(
                file_path=percorso_file, codice=codice, righe=len(df_validato), esito="OK"
            )
            ExcelLogger.log(evento)
            QMessageBox.information(
                self,
                "Importazione completata",
                f"File '{nome_file_atteso}' importato con successo.\n"
                f"{len(df_validato)} righe salvate nella tabella '{codice}'.\n\n"
                "(I record precedenti sono stati eliminati.)",
            )

        PreviewExcel(df_validato, conferma_import).exec()

    def _importa_gruppo(self, subdir_modelli: str):
        """Importa in blocco tutti i file Excel di un gruppo (sottocartella modelli)."""
        import json
        from excel.excel_loader import carica_excel
        from excel.excel_validator import ExcelValidator
        from excel.excel_importer import ExcelImporter
        from excel.excel_logger import ExcelLogger
        from ges_error.error_reporter import ErrorReporter
        from ui.error_dialog import ErrorDialog
        from ui.warning_dialog import WarningDialog
        from PySide6.QtWidgets import QDialog

        models_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "models", subdir_modelli
        )
        modelli = []
        for fname in sorted(os.listdir(models_dir)):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(models_dir, fname), "r", encoding="utf-8") as f:
                modelli.append(json.load(f))

        if not modelli:
            QMessageBox.critical(self, "Errore", f"Nessun modello trovato in '{subdir_modelli}'.")
            return

        cartella = QFileDialog.getExistingDirectory(
            self, f"Seleziona la cartella contenente i file {subdir_modelli}"
        )
        if not cartella:
            return

        # Filtra: considera solo i file attesi che sono presenti nella cartella;
        # eventuali altri xlsx presenti vengono ignorati.
        modelli_presenti = [
            m for m in modelli
            if os.path.isfile(os.path.join(cartella, m["nome_file"]))
        ]
        if not modelli_presenti:
            reporter_mancanti = ErrorReporter()
            reporter_mancanti.add(
                f"Nessun file previsto per '{subdir_modelli}' trovato nella cartella selezionata.\n"
                f"File attesi: {', '.join(m['nome_file'] for m in modelli)}"
            )
            ErrorDialog(reporter_mancanti.get_error_text()).exec()
            return

        modelli = modelli_presenti

        # Carica e valida ogni file
        dati = []  # lista di (modello, df_validato, percorso)
        tutti_errori = ErrorReporter()
        tutti_warning = ErrorReporter()

        for m in modelli:
            percorso = os.path.join(cartella, m["nome_file"])
            df = carica_excel(percorso)
            if df is None:
                tutti_errori.add(f"Impossibile leggere '{m['nome_file']}'.")
                continue
            ok, df_validato, errori, warning = ExcelValidator.valida(
                df, m.get("colonne_attese", []), m.get("tipi_colonne", None)
            )
            if not ok:
                tutti_errori.extend_errors([f"[{m['nome_file']}] {e}" for e in errori])
            else:
                dati.append((m, df_validato, percorso))
                if warning:
                    tutti_warning.extend_warnings([f"[{m['nome_file']}] {w}" for w in warning])

        if tutti_errori.has_errors():
            ErrorDialog(tutti_errori.get_error_text()).exec()
            return

        if tutti_warning.warnings:
            dlg = WarningDialog(tutti_warning.get_warning_text())
            if dlg.exec() == QDialog.DialogCode.Rejected:
                return

        # Riepilogo e conferma
        riepilogo = "\n".join(
            f"\u2022 {m['nome_file']}: {len(df)} righe" for m, df, _ in dati
        )
        risposta = QMessageBox.question(
            self,
            "Conferma importazione",
            f"Stai per importare i seguenti file:\n\n{riepilogo}\n\nI record precedenti verranno eliminati. Confermi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if risposta != QMessageBox.StandardButton.Yes:
            return

        # Importa e logga ciascun file
        for m, df_validato, percorso in dati:
            ExcelImporter.importa(m["codice"], df_validato)
            ExcelLogger.log(
                ExcelLogger.crea_evento(
                    file_path=percorso,
                    codice=m["codice"],
                    righe=len(df_validato),
                    esito="OK",
                )
            )

        QMessageBox.information(
            self,
            "Importazione completata",
            f"Importati {len(dati)} file con successo.\n(I record precedenti sono stati eliminati.)",
        )

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
