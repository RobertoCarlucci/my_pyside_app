class FileModel:
    """Definisce la struttura attesa dei file Excel."""

    MODELLI = {
        "res10": {"colonne_attese": ["Codice", "Descrizione", "Quantità", "Prezzo"]}
    }

    @classmethod
    def get_colonne_attese(cls, codice_file):
        modello = cls.MODELLI.get(codice_file)
        if modello:
            return modello["colonne_attese"]
        return None

    @classmethod
    def verifica_colonne(cls, df, codice_file):
        colonne_attese = cls.get_colonne_attese(codice_file)
        if colonne_attese is None:
            return False

        return all(col in df.columns for col in colonne_attese)
