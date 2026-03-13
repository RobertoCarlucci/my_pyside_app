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
from PySide6.QtWidgets import QDialog, QProgressDialog, QApplication
from PySide6.QtCore import Qt


class MainExcel:

    def __init__(self, parent_ui):
        """
        parent_ui = riferimento alla MainWindow Qt
        per aggiornare label o mostrare messaggi.
        """
        self.ui = parent_ui

    def start_import(self):
        """Flusso completo di importazione Excel."""

        # 1. Selezione file
        file_path = FileSelector.seleziona_excel(self.ui)
        if not file_path:
            return

        # 2. Autorizzazione
        if not FileAuthorizer.is_autorizzato(file_path):
            self.ui.label.setText("❌ File non autorizzato")
            return

        codice = FileAuthorizer.get_codice(file_path)
        if codice is None:
            self.ui.label.setText("❌ File non autorizzato")
            return

        # 3. Caricamento Excel
        df = carica_excel(file_path)
        if df is None:
            self.ui.label.setText("❌ Errore nel caricamento Excel")
            return

        # 4. Carico colonne attese dal modello JSON
        colonne_attese = FileModel.get_colonne_attese(codice)
        if not colonne_attese:
            self.ui.label.setText("❌ Modello colonne non trovato")
            return

        # 5. Carico tipi attesi dal modello JSON
        tipi_attesi = FileModel.get_tipi_colonne(codice)

        # 6. Validazione + mappatura + tipi
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
            return

        # 7. Mostra anteprima
        def conferma_import():
            # Barra di avanzamento
            totale = len(df_validato)
            progress = QProgressDialog(
                "Salvataggio in corso...", "", 0, totale, self.ui
            )
            progress.setCancelButton(None)
            progress.setWindowTitle("Importazione RES10")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            progress.show()
            QApplication.processEvents()

            def on_progress(current, total):
                progress.setValue(current)
                QApplication.processEvents()

            # IMPORTAZIONE SPECIFICA PER IL FILE
            if codice == "res10":
                ExcelImporter.importa_res10(df_validato, on_progress)
            # elif codice == "res20":
            #     ExcelImporter.importa_res20(df_validato, on_progress)

            progress.setValue(totale)
            progress.close()

            # LOG SUCCESS
            evento = ExcelLogger.crea_evento(
                file_path=file_path, codice=codice, righe=len(df_validato), esito="OK"
            )
            ExcelLogger.log(evento)

            self.ui.label.setText("✔️ Importazione completata")

        preview = PreviewExcel(df_validato, conferma_import)
        preview.exec()
