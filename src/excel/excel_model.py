import json
import os


class FileModel:
    """
    Carica e gestisce i modelli Excel definiti in JSON.
    """

    MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "update")

    @classmethod
    def load_model(cls, codice_file: str):
        """Carica il file JSON del modello richiesto."""
        path = os.path.join(cls.MODELS_DIR, f"{codice_file}.json")
        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Errore nel file di configurazione {codice_file}.json:\n"
                f"Riga {e.lineno}, Colonna {e.colno}: {e.msg}"
            ) from e
        except Exception as e:
            raise ValueError(
                f"Errore nel caricamento del modello {codice_file}: {e}"
            ) from e

    @classmethod
    def get_colonne_attese(cls, codice_file: str):
        modello = cls.load_model(codice_file)
        if modello:
            return modello.get("colonne_attese", [])
        return None

    @classmethod
    def get_tipi_colonne(cls, codice_file: str) -> dict | None:
        modello = cls.load_model(codice_file)
        if modello:
            return modello.get("tipi_colonne", None)
        return None

    @classmethod
    def verifica_colonne(cls, df, codice_file: str):
        from excel.excel_validator import ExcelValidator

        colonne_attese = cls.get_colonne_attese(codice_file)
        if not colonne_attese:
            return False, df

        ok, df_validato, _, _ = ExcelValidator.valida(df, colonne_attese)
        return ok, df_validato

    @classmethod
    def get_all_models(cls):
        """Ritorna i codici di tutti i modelli Excel disponibili.

        Filtra i JSON in cui 'nome_file' ha estensione .xlsx o .xls;
        ignora silenziosamente i file di altri tipi.
        """
        result = []
        for fname in os.listdir(cls.MODELS_DIR):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(cls.MODELS_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            nome_file = data.get("nome_file", "")
            ext = os.path.splitext(nome_file)[1].lower()
            if ext not in (".xlsx", ".xls"):
                continue
            result.append(fname.replace(".json", ""))
        return result
