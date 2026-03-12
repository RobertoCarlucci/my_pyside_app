import sqlite3
import os

# Percorso del file DB (nella cartella principale del progetto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "app.db")


def get_connection():
    """Ritorna una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)


def inserisci_res10_record(**kwargs):
    """
    Inserisce una riga del file res10 nel DB.
    kwargs contiene: colonna=valore
    """
    conn = get_connection()
    cur = conn.cursor()

    # I nomi di colonna vanno quotati perché contengono spazi e caratteri speciali
    colonne = ", ".join(f'"{col}"' for col in kwargs.keys())
    placeholders = ", ".join(["?"] * len(kwargs))
    valori = list(kwargs.values())

    sql = f"INSERT INTO res10 ({colonne}) VALUES ({placeholders})"
    cur.execute(sql, valori)

    conn.commit()
    conn.close()


def init_db():
    """Crea il database e le tabelle se non esistono."""
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS res10 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "Resource Name" TEXT,
            "Start Date" TEXT,
            "Term Date" TEXT,
            "User Name" TEXT,
            "User Role" TEXT,
            "Organizational Resource" TEXT,
            "Calendar" TEXT,
            "Hours Per Week" REAL,
            "Activity Type" TEXT,
            "Competence (Concatenated List)" TEXT,
            "Competence (Primary Value)" TEXT,
            "Competence 2" TEXT,
            "Cost Centers" TEXT,
            "Direct Supervisor Name" TEXT,
            "Direct Supervisor Name 2" TEXT,
            "Disapproved Timesheets" TEXT,
            "Email Notifications Enabled" TEXT,
            "Job Location Country" TEXT,
            "Job Location Region" TEXT,
            "Legal Entity" TEXT,
            "Network Authentication Name" TEXT,
            "Organization (OBS)" TEXT,
            "Overdue Timesheets" INTEGER,
            "Parameters" TEXT,
            "Providing Org." TEXT,
            "RES Organization" TEXT,
            "RES Seniority" TEXT,
            "Resource Comments" TEXT,
            "Resource Depth" TEXT,
            "Resource Quantity" TEXT,
            "Resource Types" TEXT,
            "Short Name" TEXT,
            "Skill (Concatenated List)" TEXT,
            "Skill (Primary Value)" TEXT,
            "Sub Org (OBS)" TEXT,
            "Team (OBS)" TEXT,
            "Teams (Concatenated List)" TEXT,
            "Teams (Primary Value)" TEXT,
            "Timesheets Submitted" INTEGER,
            "Timesheets To Approve" INTEGER,
            "User E-Mail Address" TEXT,
            "User Pager" TEXT,
            "User Phone 1" TEXT,
            "User Phone 2" TEXT,
            "Work Location" TEXT
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
