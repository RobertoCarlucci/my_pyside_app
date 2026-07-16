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
        from excel.excel_model import FileModel
        df = df.copy()
        modello = FileModel.load_model(codice)
        if modello:
            col_attese = modello.get("colonne_attese", [])
            col_escluse = set(modello.get("colonne_da_rimuovere", []))
            col_db = list(modello.get("tipi_colonne", {}).keys())

            # Rimuovi le colonne escluse prima del rename
            if col_escluse:
                df = df.drop(columns=[c for c in col_escluse if c in df.columns])

            # Rinomina: zip tra colonne_attese rimaste e chiavi tipi_colonne (positional)
            col_rimanenti = [c for c in col_attese if c not in col_escluse]
            if col_rimanenti and col_db:
                rename_map = {
                    src: dst
                    for src, dst in zip(col_rimanenti, col_db)
                    if src != dst
                }
                if rename_map:
                    df = df.rename(columns=rename_map)
        df.insert(0, "id", range(1, len(df) + 1))
        righe = [
            {col: _to_db(val) for col, val in row.items()} for _, row in df.iterrows()
        ]
        importa_bulk(codice, righe, progress_callback)
