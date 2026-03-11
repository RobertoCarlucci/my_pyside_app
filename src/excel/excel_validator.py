import pandas as pd
from datetime import datetime


class ExcelValidator:

    # ---------------------------------------------------------
    # NORMALIZZAZIONE
    # ---------------------------------------------------------
    @staticmethod
    def normalizza(testo: str) -> str:
        return " ".join(testo.strip().split()).lower()

    # ---------------------------------------------------------
    # RIMOZIONE HEADER VUOTO
    # ---------------------------------------------------------
    @staticmethod
    def rimuovi_header_vuoto(df: pd.DataFrame):
        if df.iloc[0].isna().all():
            df = df.iloc[1:].reset_index(drop=True)
        return df

    # ---------------------------------------------------------
    # MATCH COLONNE
    # ---------------------------------------------------------
    @staticmethod
    def trova_match(colonna_attesa_norm, colonne_file_norm):
        for col in colonne_file_norm:
            if colonna_attesa_norm in col:
                if len(col) >= len(colonna_attesa_norm):
                    return col
        return None

    # ---------------------------------------------------------
    # MAPPATURA COLONNE
    # ---------------------------------------------------------
    @staticmethod
    def mappa_colonne(df: pd.DataFrame, colonne_attese: list):
        errori = []

        colonne_file_norm = {ExcelValidator.normalizza(c): c for c in df.columns}
        mapping = {}

        for col_attesa in colonne_attese:
            col_attesa_norm = ExcelValidator.normalizza(col_attesa)

            col_file_norm = ExcelValidator.trova_match(
                col_attesa_norm, colonne_file_norm.keys()
            )

            if not col_file_norm:
                errori.append(f"Colonna mancante o troncata: {col_attesa}")
                continue

            mapping[col_attesa] = colonne_file_norm[col_file_norm]

        if errori:
            return False, df, errori

        df = df.rename(columns={v: k for k, v in mapping.items()})
        return True, df, []

    # ---------------------------------------------------------
    # VALIDAZIONE TIPI
    # ---------------------------------------------------------
    @staticmethod
    def valida_tipi(df: pd.DataFrame, tipi_attesi: dict):
        """
        tipi_attesi = { "Colonna": "int" | "float" | "date" | "str" }
        """
        errori = []

        for col, tipo in tipi_attesi.items():

            if col not in df.columns:
                errori.append(f"Colonna '{col}' non trovata per validazione tipi")
                continue

            serie = df[col]

            # INT
            if tipo == "int":
                try:
                    df[col] = pd.to_numeric(serie, errors="raise").astype("Int64")
                except:
                    errori.append(f"Valori non validi per INT nella colonna '{col}'")

            # FLOAT
            elif tipo == "float":
                try:
                    serie = serie.astype(str).str.replace(",", ".")
                    df[col] = pd.to_numeric(serie, errors="raise").astype(float)
                except:
                    errori.append(f"Valori non validi per FLOAT nella colonna '{col}'")

            # DATE
            elif tipo == "date":
                try:
                    df[col] = pd.to_datetime(serie, errors="raise", dayfirst=True)
                except:
                    errori.append(f"Valori non validi per DATE nella colonna '{col}'")

            # STRING
            elif tipo == "str":
                df[col] = serie.astype(str)

        if errori:
            return False, df, errori

        return True, df, []

    # ---------------------------------------------------------
    # VALIDAZIONE COMPLETA
    # ---------------------------------------------------------
    @staticmethod
    def valida(df: pd.DataFrame, colonne_attese: list, tipi_attesi: dict | None = None):
        """
        1. Rimuove header vuoto
        2. Mappa colonne
        3. Valida tipi (se presenti)
        """
        df = ExcelValidator.rimuovi_header_vuoto(df)

        ok, df, errori = ExcelValidator.mappa_colonne(df, colonne_attese)
        if not ok:
            return False, df, errori

        if tipi_attesi:
            ok, df, errori_tipi = ExcelValidator.valida_tipi(df, tipi_attesi)
            if not ok:
                return False, df, errori + errori_tipi

        return True, df, []
