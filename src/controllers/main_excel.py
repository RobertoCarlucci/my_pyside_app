from excel.file_selector import FileSelector
from excel.file_authorizer import FileAuthorizer
from excel.file_model import FileModel
from excel.excel_loader import carica_excel
from excel.excel_validator import ExcelValidator
from excel.excel_importer import ExcelImporter
from ui.preview_excel import PreviewExcel


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
        ok, df_validato, errori = ExcelValidator.valida(df, colonne_attese, tipi_attesi)

        if not ok:
            self.ui.label.setText("❌ Errori nella struttura del file")
            print("Errori:", errori)
            return

        # 7. Mostra anteprima
        def conferma_import():
            # IMPORTAZIONE SPECIFICA PER IL FILE
            if codice == "res10":
                ExcelImporter.importa_res10(df_validato)
            # elif codice == "res20":
            #     ExcelImporter.importa_res20(df_validato)
            # elif codice == "res30":
            #     ExcelImporter.importa_res30(df_validato)

            self.ui.label.setText("✔️ Importazione completata")

        preview = PreviewExcel(df_validato, conferma_import)
        preview.exec()
