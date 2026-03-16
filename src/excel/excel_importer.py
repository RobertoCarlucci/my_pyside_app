import pandas as pd

from db.database import inserisci_res10_bulk


def _to_sqlite(val):
    """Converte un valore pandas in un tipo nativo Python compatibile con sqlite3."""
    # pd.Timestamp → datetime.date nativo (SQLite lo gestisce direttamente)
    if isinstance(val, pd.Timestamp):
        if pd.isnull(val):
            return None
        # Se ha componente oraria significativa → DATETIME, altrimenti → DATE
        if val.hour == 0 and val.minute == 0 and val.second == 0:
            return val.strftime("%Y-%m-%d")
        return val.strftime("%Y-%m-%d %H:%M:%S")

    # Gestisci NaT (Not-a-Time)
    if pd.isna(val):
        return None

    # pandas Int64 / numpy integer → int Python
    if hasattr(val, "item"):
        return val.item()

    return val


class ExcelImporter:

    @staticmethod
    def importa(codice: str, df, progress_callback=None):
        """
        Importa i dati del file res10 nel DB in un'unica transazione.
        df = DataFrame validato e mappato
        progress_callback(current, total): opzionale, per aggiornare la UI.
        """
        righe = [
            {col: _to_sqlite(val) for col, val in row.items()}
            for _, row in df.iterrows()
        ]
        inserisci_res10_bulk(righe, progress_callback)
