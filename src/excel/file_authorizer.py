import os


class FileAuthorizer:
    """Controlla se un file Excel è autorizzato all'import."""

    FILE_CONOSCIUTI = {"RES10.xlsx": "res10"}  # puoi associare un codice interno

    @classmethod
    def is_autorizzato(cls, file_path: str) -> bool:
        nome = os.path.basename(file_path)
        return nome in cls.FILE_CONOSCIUTI

    @classmethod
    def get_codice(cls, file_path: str):
        nome = os.path.basename(file_path)
        return cls.FILE_CONOSCIUTI.get(nome)
