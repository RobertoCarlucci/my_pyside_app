import os
from excel.file_model import FileModel


class FileAuthorizer:
    """
    Autorizza i file Excel confrontando il nome con i modelli JSON.
    """

    @classmethod
    def is_autorizzato(cls, file_path: str) -> bool:
        nome = os.path.basename(file_path)

        for codice in FileModel.get_all_models():
            modello = FileModel.load_model(codice)
            if modello and modello["nome_file"] == nome:
                return True

        return False

    @classmethod
    def get_codice(cls, file_path: str):
        nome = os.path.basename(file_path)

        for codice in FileModel.get_all_models():
            modello = FileModel.load_model(codice)
            if modello and modello["nome_file"] == nome:
                return modello["codice"]

        return None
