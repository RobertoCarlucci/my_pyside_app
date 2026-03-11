from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class PreviewExcel(QDialog):

    def __init__(self, df, on_confirm):
        super().__init__()

        self.setWindowTitle("Anteprima importazione Excel")
        self.resize(900, 600)

        self.df = df
        self.on_confirm = on_confirm

        layout = QVBoxLayout()

        # Titolo
        titolo = QLabel("Controlla i dati e conferma l'importazione")
        titolo.setAlignment(Qt.AlignCenter)
        titolo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titolo)

        # Tabella anteprima
        table = QTableWidget()
        max_rows = min(20, len(df))
        table.setRowCount(max_rows)
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for r in range(max_rows):
            for c, col in enumerate(df.columns):
                value = str(df.iloc[r][col])
                table.setItem(r, c, QTableWidgetItem(value))

        layout.addWidget(table)

        # Pulsanti
        buttons = QHBoxLayout()

        btn_cancel = QPushButton("Annulla")
        btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(btn_cancel)

        btn_confirm = QPushButton("Conferma importazione")
        btn_confirm.clicked.connect(self.conferma)
        buttons.addWidget(btn_confirm)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def conferma(self):
        """Richiama la funzione di importazione e chiude la finestra."""
        self.on_confirm()
        self.accept()
