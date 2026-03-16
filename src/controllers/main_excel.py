from excel.file_selector import FileSelector
from excel.file_authorizer import FileAuthorizer
from excel.file_model import FileModel
from excel.excel_loader import carica_excel
from excel.excel_validator import ExcelValidator
from excel.excel_importer import ExcelImporter

from ges_error.error_reporter import ErrorReporter
from ui.error_dialog import ErrorDialog
from ui.preview_excel import PreviewExcel
from ui.warning_dialog import WarningDialog
from excel.excel_logger import ExcelLogger
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QThread, Signal


class _ImportWorker(QThread):
    """Esegue l'import su un thread separato per non bloccare la UI."""

    progress = Signal(int, int)  # (current, total)
    finished = Signal()
    error = Signal(str)

    def __init__(self, codice: str, df, parent=None):
        super().__init__(parent)
        self._codice = codice
        self._df = df

    def run(self):
        try:
            ExcelImporter.importa(
                self._codice,
                self._df,
                progress_callback=lambda c, t: self.progress.emit(c, t),
            )
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainExcel:

    def __init__(self, parent_ui):
        """
        parent_ui = riferimento alla MainWindow Qt
        per aggiornare label o mostrare messaggi.
        """
        self.ui = parent_ui
        self._worker = None  # mantiene il riferimento al thread attivo

    def start_import(self):
        """Flusso completo di importazione Excel."""

        # Blocca subito il pulsante per evitare doppi avvii
        self.ui.btn_importa.setEnabled(False)
        self.ui.label.setText("")

        def _ripristina():
            self.ui.btn_importa.setEnabled(True)

        # 1. Selezione file
        file_path = FileSelector.seleziona_excel(self.ui)
        if not file_path:
            _ripristina()
            return

        # 2. Autorizzazione
        if not FileAuthorizer.is_autorizzato(file_path):
            self.ui.label.setText("❌ File non autorizzato")
            _ripristina()
            return

        codice = FileAuthorizer.get_codice(file_path)
        if codice is None:
            self.ui.label.setText("❌ File non autorizzato")
            _ripristina()
            return

        # 3. Caricamento Excel
        self.ui.label.setText("⏳ Caricamento file...")
        df = carica_excel(file_path)
        if df is None:
            self.ui.label.setText("❌ Errore nel caricamento Excel")
            _ripristina()
            return

        # 4. Colonne attese dal modello JSON
        colonne_attese = FileModel.get_colonne_attese(codice)
        if not colonne_attese:
            self.ui.label.setText("❌ Modello colonne non trovato")
            _ripristina()
            return

        # 5. Tipi attesi dal modello JSON
        tipi_attesi = FileModel.get_tipi_colonne(codice)

        # 6. Validazione + mappatura + tipi
        self.ui.label.setText("⏳ Validazione in corso...")
        ok, df_validato, errori, warning = ExcelValidator.valida(
            df, colonne_attese, tipi_attesi
        )

        # ERRORI → bloccanti
        if errori:
            reporter = ErrorReporter()
            reporter.extend_errors(errori)
            dlg = ErrorDialog(reporter.get_error_text())
            dlg.exec()
            self.ui.label.setText("❌ Importazione annullata")
            _ripristina()
            return

        # WARNING → chiedi conferma
        risposta = QDialog.DialogCode.Accepted
        if warning:
            reporter = ErrorReporter()
            reporter.extend_warnings(warning)
            dlg = WarningDialog(reporter.get_warning_text())
            risposta = dlg.exec()

        if risposta == QDialog.DialogCode.Rejected:
            self.ui.label.setText("⚠️ Importazione annullata dall'utente")
            _ripristina()
            return

        # 7. Mostra anteprima
        def conferma_import():
            totale = len(df_validato)
            self.ui.progress_bar.setMaximum(totale)
            self.ui.progress_bar.setValue(0)
            self.ui.label.setText("⏳ Salvataggio in corso...")

            worker = _ImportWorker(codice, df_validato, self.ui)
            worker.progress.connect(lambda c, _t: self.ui.progress_bar.setValue(c))

            def _on_finished():
                self.ui.progress_bar.setValue(totale)
                # btn_importa resta disabilitato: l'utente deve premere "Nuova Importazione"
                self.ui.btn_nuova.setEnabled(True)
                self.ui.label.setText("✔️ Importazione completata")
                evento = ExcelLogger.crea_evento(
                    file_path=file_path, codice=codice, righe=totale, esito="OK"
                )
                ExcelLogger.log(evento)

            def _on_error(msg: str):
                _ripristina()
                self.ui.label.setText(f"❌ Errore: {msg}")

            worker.finished.connect(_on_finished)
            worker.error.connect(_on_error)
            self._worker = worker
            worker.start()

        preview = PreviewExcel(df_validato, conferma_import)
        if preview.exec() == QDialog.DialogCode.Rejected:
            self.ui.label.setText("")
            _ripristina()
