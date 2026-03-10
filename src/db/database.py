import sqlite3
import os

# Percorso del file DB (nella cartella principale del progetto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "app.db")


def get_connection():
    """Ritorna una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Crea il database e la tabella se non esistono."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def inserisci_utente(nome: str):
    """Inserisce un utente nella tabella utenti."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO utenti (nome) VALUES (?)",
        (nome,),
    )

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
