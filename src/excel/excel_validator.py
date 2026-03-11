import pandas as pd


class ExcelValidator:

    @staticmethod
    def normalizza(testo: str) -> str:
        return " ".join(testo.strip().split()).lower()

    @staticmethod
    def rimuovi_header_vuoto(df: pd.DataFrame):
        if df.iloc[0].isna().all():
            df = df.iloc[1:].reset_index(drop=True)
        return df

    @staticmethod
    def trova_match(colonna_attesa_norm, colonne_file_norm):
        for col in colonne_file_norm:
            if colonna_attesa_norm in col:
                if len(col) >= len(colonna_attesa_norm):
                    return col
        return None

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

    @staticmethod
    def valida(df: pd.DataFrame, colonne_attese: list):
        """
        Metodo principale di validazione.
        1. Rimuove header vuoto
        2. Mappa colonne
        3. Restituisce (ok, df_validato, errori)
        """
        df = ExcelValidator.rimuovi_header_vuoto(df)
        ok, df_mappato, errori = ExcelValidator.mappa_colonne(df, colonne_attese)
        return ok, df_mappato, errori
