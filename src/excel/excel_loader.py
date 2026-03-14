import pandas as pd
import logging

logger = logging.getLogger(__name__)


def carica_excel(percorso_file):
    """Carica un file Excel e ritorna un DataFrame.

    Args:
        percorso_file: Percorso del file Excel

    Returns:
        DataFrame se il caricamento ha successo, None altrimenti
    """
    try:
        df = pd.read_excel(percorso_file)
        logger.info(f"File Excel caricato: {percorso_file}")
        logger.info(f"Colonne trovate: {list(df.columns)}")
        logger.info(f"Numero di righe: {len(df)}")
        print(f"✓ File caricato con {len(df)} righe")
        print(f"✓ Colonne: {list(df.columns)}")
        return df
    except FileNotFoundError:
        msg = f"File non trovato: {percorso_file}"
        logger.error(msg)
        print(f"❌ {msg}")
        return None
    except Exception as e:
        msg = f"Errore durante il caricamento del file Excel: {type(e).__name__}: {e}"
        logger.error(msg, exc_info=True)
        print(f"❌ {msg}")
        return None
