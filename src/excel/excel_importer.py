import pandas as pd

from db.database import inserisci_res10_record


class ExcelImporter:

    @staticmethod
    def importa_res10(df):
        """
        Importa i dati del file res10 nel DB.
        df = DataFrame validato e mappato
        """

        for _, row in df.iterrows():
            # Convertiamo NaN in None per SQLite
            dati = {col: (None if pd.isna(val) else val) for col, val in row.items()}

            inserisci_res10_record(**dati)
