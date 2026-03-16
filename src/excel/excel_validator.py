import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


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
        """
        Mappa le colonne del file con quelle attese.
        Richiede: ESATTO numero di colonne.
        Tolleranza: nomi parzialmente uguali (matching).
        """
        errori = []

        # 1) Controlla numero ESATTO di colonne
        if len(df.columns) != len(colonne_attese):
            msg = f"Numero di colonne non corrisponde: file ha {len(df.columns)}, attese {len(colonne_attese)}"
            logger.error(msg)
            errori.append(msg)
            return False, df, errori

        colonne_file_norm = {ExcelValidator.normalizza(c): c for c in df.columns}
        mapping = {}

        # 2) Fai il matching per nome (tollerante)
        for col_attesa in colonne_attese:
            col_attesa_norm = ExcelValidator.normalizza(col_attesa)

            # Cerca un match esatto prima
            if col_attesa_norm in colonne_file_norm:
                mapping[col_attesa] = colonne_file_norm[col_attesa_norm]
                continue

            # Poi cerca un match parziale (col_attesa_norm contenuto in col_file_norm)
            col_file_norm = ExcelValidator.trova_match(
                col_attesa_norm, colonne_file_norm.keys()
            )

            if col_file_norm:
                mapping[col_attesa] = colonne_file_norm[col_file_norm]
            else:
                msg = f"Colonna '{col_attesa}' non trovata nel file"
                logger.error(msg)
                errori.append(msg)

        if errori:
            return False, df, errori

        df = df.rename(columns={v: k for k, v in mapping.items()})
        return True, df, []

    # ---------------------------------------------------------
    # NUOVO: TROVA COLONNE EXTRA
    # ---------------------------------------------------------
    @staticmethod
    def trova_colonne_extra(df: pd.DataFrame, colonne_attese: list):
        """
        Restituisce una lista di colonne presenti nel file
        ma NON previste dal modello.
        """
        colonne_extra = []

        for col in df.columns:
            if col not in colonne_attese:
                colonne_extra.append(col)

        return colonne_extra

    # ---------------------------------------------------------
    # VALIDAZIONE TIPI
    # ---------------------------------------------------------
    @staticmethod
    def valida_tipi(df: pd.DataFrame, tipi_attesi: dict):
        """
        tipi_attesi = { "Colonna": "int" | "float" | "date" | "string" }
        Converte i tipi in modo tollerante: NULL rimangono NULL,
        errori di conversione diventano NULL anzichè bloccare.
        """
        errori = []

        for col, tipo in tipi_attesi.items():

            if col not in df.columns:
                # Colonna mancante è warning, non errore
                logger.warning(f"Colonna '{col}' non trovata nel file")
                continue

            serie = df[col]

            # INT
            if tipo == "int":
                try:
                    # Converti con coerce per trasformare errori a NaN
                    df[col] = pd.to_numeric(serie, errors="coerce").astype("Int64")
                except:
                    logger.error(f"Errore conversione INT per '{col}'")
                    pass

            # FLOAT
            elif tipo == "float":
                try:
                    # Gestisci virgole come separatori decimali
                    serie_str = serie.astype(str).str.replace(",", ".")
                    df[col] = pd.to_numeric(serie_str, errors="coerce").astype(float)
                except:
                    logger.error(f"Errore conversione FLOAT per '{col}'")
                    pass

            # DATE
            elif tipo == "date":
                try:
                    # Se è già datetime64, mantienila
                    if pd.api.types.is_datetime64_any_dtype(serie):
                        df[col] = serie
                    else:
                        # Altrimenti converti, trasformando errori a NaT
                        df[col] = pd.to_datetime(serie, errors="coerce", dayfirst=True)
                except:
                    logger.error(f"Errore conversione DATE per '{col}'")
                    pass

            # STRING (o tutto il resto)
            else:
                try:
                    df[col] = serie.astype(str)
                except:
                    logger.error(f"Errore conversione STRING per '{col}'")
                    pass

        # Non ritorniamo errori - i dati vengono comunque convertiti al meglio
        return True, df, []

    # ---------------------------------------------------------
    # VALIDAZIONE COMPLETA (AGGIORNATA)
    # ---------------------------------------------------------
    @staticmethod
    def valida(df: pd.DataFrame, colonne_attese: list, tipi_attesi: dict | None = None):
        """
        1. Rimuove header vuoto
        2. Mappa colonne
        3. Warning colonne extra
        4. Valida tipi (se presenti)
        """
        df = ExcelValidator.rimuovi_header_vuoto(df)

        # 1) Mappatura colonne
        ok, df, errori = ExcelValidator.mappa_colonne(df, colonne_attese)
        if not ok:
            return False, df, errori, []

        # 2) Colonne extra → WARNING
        warning = []
        colonne_extra = ExcelValidator.trova_colonne_extra(df, colonne_attese)
        for col in colonne_extra:
            warning.append(f"Colonna extra non prevista: {col}")

        # 3) Validazione tipi
        if tipi_attesi:
            ok, df, errori_tipi = ExcelValidator.valida_tipi(df, tipi_attesi)
            if not ok:
                return False, df, errori_tipi, warning

        return True, df, [], warning
