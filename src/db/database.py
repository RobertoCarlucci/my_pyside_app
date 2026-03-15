import sqlite3
import os
import json
import glob

# Percorso del file DB (nella cartella src del progetto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "app.db")

MODELS_DIR = os.path.join(BASE_DIR, "excel", "models")

# Mapping tipi JSON/Python → tipi SQLite
_TIPO_MAP = {
    "string": "TEXT",
    "str":    "TEXT",
    "text":   "TEXT",
    "int":    "INTEGER",
    "integer":"INTEGER",
    "float":  "REAL",
    "real":   "REAL",
    "date":   "TEXT",
    "datetime":"TEXT",
}


def _tipo_sqlite(tipo: str) -> str:
    """Converte un tipo JSON/Python nel corrispondente tipo SQLite."""
    return _TIPO_MAP.get(tipo.lower(), "TEXT")


def _carica_modelli() -> list[dict]:
    """Carica tutti i modelli JSON dalla cartella models."""
    modelli = []
    for path in glob.glob(os.path.join(MODELS_DIR, "*.json")):
        with open(path, encoding="utf-8") as f:
            modelli.append(json.load(f))
    return modelli


def get_connection():
    """Ritorna una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)


def inserisci_record(tabella: str, **kwargs):
    """Inserisce una singola riga nella tabella specificata."""
    colonne_sql = ", ".join(f'"{c}"' for c in kwargs.keys())
    placeholders = ", ".join(["?"] * len(kwargs))
    sql = f'INSERT INTO "{tabella}" ({colonne_sql}) VALUES ({placeholders})'
    conn = get_connection()
    try:
        conn.execute(sql, list(kwargs.values()))
        conn.commit()
    finally:
        conn.close()


def inserisci_bulk(tabella: str, righe: list[dict], progress_callback=None):
    """
    Inserisce tutte le righe nella tabella specificata in un'unica transazione.
    Svuota la tabella prima del caricamento.
    righe: lista di dict {colonna: valore} già convertiti in tipi Python nativi.
    progress_callback(current, total): chiamato dopo ogni batch.
    """
    if not righe:
        return

    colonne = list(righe[0].keys())
    colonne_sql = ", ".join(f'"{c}"' for c in colonne)
    placeholders = ", ".join(["?"] * len(colonne))
    sql = f'INSERT INTO "{tabella}" ({colonne_sql}) VALUES ({placeholders})'

    valori = [tuple(r[c] for c in colonne) for r in righe]
    totale = len(valori)
    BATCH = 100

    conn = get_connection()
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f'DELETE FROM "{tabella}"')
        for i in range(0, totale, BATCH):
            conn.executemany(sql, valori[i : i + BATCH])
            if progress_callback:
                progress_callback(min(i + BATCH, totale), totale)
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Crea il database e le tabelle se non esistono, leggendo i modelli JSON."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabella utenti (non legata a un modello JSON)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """
    )

    # Tabelle dei modelli Excel: struttura letta dai JSON
    for modello in _carica_modelli():
        tabella = modello["codice"]
        col_defs = [
            f'    "{col}" {_tipo_sqlite(tipo)}'
            for col, tipo in modello["tipi_colonne"].items()
        ]
        sql = (
            f'CREATE TABLE IF NOT EXISTS "{tabella}" (\n'
            f'    id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
            + ",\n".join(col_defs)
            + "\n)"
        )
        cursor.execute(sql)

    conn.commit()
    conn.close()


def inserisci_utente(nome: str):
    """Inserisce un utente nella tabella utenti."""
    inserisci_record("utenti", nome=nome)


def lista_utenti():
    """Ritorna la lista di tutti gli utenti (id, nome)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM utenti")
    rows = cursor.fetchall()
    conn.close()
    return rows
