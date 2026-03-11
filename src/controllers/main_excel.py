from excel.file_selector import FileSelector
from excel.file_authorizer import FileAuthorizer
from excel.file_model import FileModel
from excel.excel_loader import carica_excel
from excel.excel_validator import ExcelValidator
from excel.excel_importer import ExcelImporter
from ui.preview_excel import PreviewExcel


class MainExcel:

    def __init__(self, parent_ui):
        self.ui = parent_ui

    def start_import(self):
        file_path = FileSelector.seleziona_excel(self.ui)
        if not file_path:
            return

        if not FileAuthorizer.is_autorizzato(file_path):
            self.ui.label.setText("❌ File non autorizzato")
            return

        codice = FileAuthorizer.get_codice(file_path)

        df = carica_excel(file_path)
        if df is None:
            self.ui.label.setText("❌ Errore nel caricamento Excel")
            return

        colonne_attese = FileModel.get_colonne_attese(codice)
        if not colonne_attese:
            self.ui.label.setText("❌ Modello colonne non trovato")
            return

        ok, df_validato, errori = ExcelValidator.valida(df, colonne_attese)

        if not ok:
            self.ui.label.setText("❌ Errori nella struttura del file")
            print(errori)
            return

        def conferma_import():
            if codice == "res10":
                ExcelImporter.importa_res10(df_validato)
            self.ui.label.setText("✔️ Importazione completata")

        preview = PreviewExcel(df_validato, conferma_import)
        preview.exec()
