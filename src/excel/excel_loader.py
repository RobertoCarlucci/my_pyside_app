import pandas as pd


def carica_excel(percorso_file):
    try:
        df = pd.read_excel(percorso_file)
        return df
    except Exception as e:
        print("Errore durante il caricamento del file Excel:", e)
        return None
