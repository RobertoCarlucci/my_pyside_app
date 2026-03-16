import pandas as pd

from db.database import importa_bulk


def _to_sqlite(val):
    """Converte un valore pandas in un tipo nativo Python compatibile con sqlite3."""
    # pd.Timestamp → datetime.date nativo
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
    def importa(codice: str, df, progress_callback=None):
        """
        Importa un DataFrame nel DB nella tabella corrispondente al codice.
        Funziona per qualsiasi modello definito in JSON.
        progress_callback(current, total): opzionale, per aggiornare la UI.
        """
        righe = [
            {col: _to_sqlite(val) for col, val in row.items()}
            for _, row in df.iterrows()
        ]
        importa_bulk(codice, righe, progress_callback)
