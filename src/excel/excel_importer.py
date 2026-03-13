import pandas as pd

from db.database import inserisci_res10_bulk


def _to_sqlite(val):
    """Converte un valore pandas in un tipo nativo Python compatibile con sqlite3."""
    # pd.Timestamp → datetime.date nativo (SQLite lo gestisce direttamente)
    if isinstance(val, pd.Timestamp):
        return val.date() if not pd.isnull(val) else None
    # NA / NaN / NaT → None (NULL in SQLite)
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    # pandas Int64 / numpy integer → int Python
    if hasattr(val, "item"):
        return val.item()
    return val


class ExcelImporter:

    @staticmethod
    def importa_res10(df):
        """
        Importa i dati del file res10 nel DB in un'unica transazione.
        df = DataFrame validato e mappato
        """
        righe = [
            {col: _to_sqlite(val) for col, val in row.items()}
            for _, row in df.iterrows()
        ]
        inserisci_res10_bulk(righe)
