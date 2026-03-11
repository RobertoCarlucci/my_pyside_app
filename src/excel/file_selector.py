from PySide6.QtWidgets import QFileDialog


class FileSelector:
    """Gestisce la selezione di un file Excel dal disco."""

    @staticmethod
    def seleziona_excel(parent=None):
        file_path, _ = QFileDialog.getOpenFileName(
            parent, "Seleziona un file Excel", "", "File Excel (*.xlsx *.xls)"
        )
        return file_path
