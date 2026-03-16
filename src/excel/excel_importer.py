import pandas as pd

from db.database import importa_bulk


def _to_db(val):
    """Converte un valore pandas in un tipo nativo Python compatibile con SQLite e MariaDB."""
    # pd.Timestamp → datetime.date nativo (SQLite lo gestisce direttamente)
    if isinstance(val, pd.Timestamp):
        if pd.isnull(val):
            return None
        # Se ha componente oraria significativa → DATETIME, altrimenti → DATE
        if val.hour == 0 and val.minute == 0 and val.second == 0:
            return val.strftime("%Y-%m-%d")
        return val.strftime("%Y-%m-%d %H:%M:%S")

    # Gestisci NaT (Not-a-Time)
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
            {col: _to_db(val) for col, val in row.items()} for _, row in df.iterrows()
        ]
        importa_bulk(codice, righe, progress_callback)
