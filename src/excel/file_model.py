import json
import os
from excel.excel_validator import ExcelValidator


class FileModel:
    """
    Carica e gestisce i modelli Excel definiti in JSON.
    """

    MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

    @classmethod
    def load_model(cls, codice_file: str):
        """Carica il file JSON del modello richiesto."""
        path = os.path.join(cls.MODELS_DIR, f"{codice_file}.json")
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_colonne_attese(cls, codice_file: str):
        modello = cls.load_model(codice_file)
        if modello:
            return modello.get("colonne_attese", [])
        return None

    @classmethod
    def verifica_colonne(cls, df, codice_file: str):
        colonne_attese = cls.get_colonne_attese(codice_file)
        if not colonne_attese:
            return False, df

        ok, df_validato = ExcelValidator.valida(df, colonne_attese)
        return ok, df_validato

    @classmethod
    def get_all_models(cls):
        """Ritorna tutti i modelli disponibili leggendo i JSON."""
        files = os.listdir(cls.MODELS_DIR)
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
