import json
import os
from datetime import datetime


class ExcelLogger:

    LOG_FILE = "import_log.json"

    @staticmethod
    def log(event: dict):
        """
        event = {
            "timestamp": "...",
            "file_path": "...",
            "codice": "...",
            "righe": 123,
            "esito": "OK" | "ERROR",
            "errori": [...]
        }
        """

        # Se il file non esiste, creiamo una lista vuota
        if not os.path.exists(ExcelLogger.LOG_FILE):
            with open(ExcelLogger.LOG_FILE, "w") as f:
                json.dump([], f, indent=4)

        # Carichiamo il log esistente
        with open(ExcelLogger.LOG_FILE, "r") as f:
            data = json.load(f)

        # Aggiungiamo l'evento
        data.append(event)

        # Riscriviamo il file
        with open(ExcelLogger.LOG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def crea_evento(file_path, codice, righe, esito, errori=None):
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_path": file_path,
            "codice": codice,
            "righe": righe,
            "esito": esito,
            "errori": errori or [],
        }
