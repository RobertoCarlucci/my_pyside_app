import pandas as pd

from db.database import inserisci_res10_bulk, inserisci_pvtotaluptd_bulk


def _to_sqlite(val):
    """Converte un valore pandas in un tipo nativo Python compatibile con sqlite3.

    - Timestamp → YYYY-MM-DD string (ISO format per SQLite)
    - NaT/None → None (NULL)
    - Int64 → int
    - Resto → valore nativo
    """
    # Gestisci Timestamp (datetime) → ISO string
    if isinstance(val, pd.Timestamp):
        if pd.isnull(val):
            return None
        # Ritorna ISO format string (YYYY-MM-DD HH:MM:SS)
        return val.isoformat()

    # Gestisci NaT (Not-a-Time)
    if pd.isna(val):
        return None

    # pandas Int64 / numpy integer → int Python
    if hasattr(val, "item"):
        return val.item()

    return val


class ExcelImporter:

    @staticmethod
    def importa_res10(df, progress_callback=None):
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

    @staticmethod
    def importa_pvtotaluptd(df, progress_callback=None):
        """
        Importa i dati del file pvtotaluptd nel DB in un'unica transazione.
        df = DataFrame validato e mappato
        progress_callback(current, total): opzionale, per aggiornare la UI.
        """
        righe = [
            {col: _to_sqlite(val) for col, val in row.items()}
            for _, row in df.iterrows()
        ]
        inserisci_pvtotaluptd_bulk(righe, progress_callback)
