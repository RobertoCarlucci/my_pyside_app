import os
import sqlite3

# Percorso del database (project_root/app.db)
DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app.db")
)

# Cartella radice dei modelli JSON (le sottocartelle vengono cercate ricorsivamente)
_MODELS_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
)


def _trova_model_path(tabella: str) -> str | None:
    """Cerca ricorsivamente in _MODELS_ROOT il file JSON il cui campo 'codice' == tabella."""
    import json as _json
    for root, _dirs, files in os.walk(_MODELS_ROOT):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    data = _json.load(f)
                if data.get("codice") == tabella:
                    return path
            except Exception:
                continue
    return None

# Mapping tipi JSON → SQL (compatibile SQLite e MariaDB)
# SQLite accetta DATE/DATETIME come alias di TEXT affinity;
# MariaDB li riconosce come tipi nativi.

_TIPO_SQL: dict[str, str] = {
    "string": "TEXT",
    "str": "TEXT",
    "text": "TEXT",
    "date": "DATE",
    "datetime": "DATETIME",
    "float": "REAL",
    "real": "REAL",
    "int": "INTEGER",
    "integer": "INTEGER",
}


def get_connection():
    """Ritorna una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)


def _crea_tabella_se_assente(conn: sqlite3.Connection, tabella: str):
    """
    Verifica se la tabella esiste nel DB; se non esiste la crea leggendo
    la struttura dal file JSON corrispondente nella cartella models/.
    Solleva FileNotFoundError se il modello JSON non e` trovato.
    Solleva ValueError se il JSON non contiene le chiavi attese.
    """
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabella,)
    )
    if cur.fetchone() is not None:
        return  # tabella gia` presente

    import json

    model_path = _trova_model_path(tabella)
    if model_path is None:
        raise FileNotFoundError(
            f"Modello JSON non trovato per la tabella '{tabella}' in: {_MODELS_ROOT}"
        )

    with open(model_path, encoding="utf-8") as f:
        modello = json.load(f)

    tipi = modello.get("tipi_colonne", {})
    colonne = modello.get("colonne_attese", [])
    if not tipi and not colonne:
        raise ValueError(f"Il modello '{tabella}' non contiene 'tipi_colonne' né 'colonne_attese'.")

    if tipi:
        cols_sql = ",\n    ".join(
            f'"{col_db}" {_TIPO_SQL.get(tipo_str.lower(), tipo_str)}'
            for col_db, tipo_str in tipi.items()
        )
    else:
        cols_sql = ",\n    ".join(f'"{c}" TEXT' for c in colonne)
    conn.execute(
        f'CREATE TABLE IF NOT EXISTS "{tabella}" (\n'
        f"    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
        f"    {cols_sql}\n)"
    )


def crea_tabelle_modelli(modelli: list[dict]):
    """
    Crea (se non esistono) le tabelle per tutti i modelli Excel.
    modelli: lista di dict caricati dai file JSON (chiavi: codice, colonne_attese, tipi_colonne).
    """
    conn = get_connection()
    try:
        for modello in modelli:
            tabella = modello.get("codice")
            tipi = modello.get("tipi_colonne", {})
            colonne = modello.get("colonne_attese", [])
            if not tabella or (not tipi and not colonne):
                continue
            if tipi:
                cols_sql = ",\n    ".join(
                    f'"{col_db}" {_TIPO_SQL.get(tipo_str.lower(), tipo_str)}'
                    for col_db, tipo_str in tipi.items()
                )
            else:
                cols_sql = ",\n    ".join(f'"{c}" TEXT' for c in colonne)
            conn.execute(
                f'CREATE TABLE IF NOT EXISTS "{tabella}" (\n'
                f"    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                f"    {cols_sql}\n)"
            )
        conn.commit()
    finally:
        conn.close()


def inserisci_record(tabella: str, **kwargs):
    """
    Inserisce un singolo record nella tabella indicata.
    Crea la tabella se non esiste (legge il modello JSON corrispondente).
    kwargs: colonna=valore già convertiti in tipi Python nativi.
    """
    colonne_sql = ", ".join(f'"{c}"' for c in kwargs)
    placeholders = ", ".join(["?"] * len(kwargs))
    sql = f'INSERT INTO "{tabella}" ({colonne_sql}) VALUES ({placeholders})'

    conn = get_connection()
    try:
        _crea_tabella_se_assente(conn, tabella)
        conn.execute(sql, list(kwargs.values()))
        conn.commit()
    finally:
        conn.close()


def importa_bulk(tabella: str, righe: list[dict], progress_callback=None):
    """
    Svuota la tabella e inserisce tutte le righe in un'unica transazione.
    Se la tabella non esiste la crea leggendo il modello JSON corrispondente.
    tabella: nome della tabella SQLite (coincide con il codice del modello JSON).
    righe: lista di dict {colonna: valore} gia` convertiti in tipi Python nativi.
    progress_callback(current, total): chiamato dopo ogni batch di 100 righe.
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
        _crea_tabella_se_assente(conn, tabella)  # crea se non esiste
        conn.execute(f'DELETE FROM "{tabella}"')  # svuota prima del caricamento
        for i in range(0, totale, BATCH):
            conn.executemany(sql, valori[i : i + BATCH])
            if progress_callback:
                progress_callback(min(i + BATCH, totale), totale)
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Crea il database e la tabella utenti se non esiste."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """)
    conn.commit()
    conn.close()


def inserisci_utente(nome: str):
    """Inserisce un utente nella tabella utenti."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utenti (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()


def lista_utenti():
    """Ritorna la lista di tutti gli utenti (id, nome)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM utenti")
    rows = cursor.fetchall()
    conn.close()
    return rows
