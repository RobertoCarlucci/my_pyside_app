import pandas as pd


class ExcelImporter:

    @staticmethod
    def importa_res10(df: pd.DataFrame):
        """Importa i dati del file RES10 nel database."""
        # TODO: implementare la logica di persistenza
        print(f"[ExcelImporter] importa_res10: {len(df)} righe da importare")
