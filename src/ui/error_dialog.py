from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt


class ErrorDialog(QDialog):

    def __init__(self, error_text: str):
        super().__init__()

        self.setWindowTitle("Errori durante l'importazione")
        self.resize(600, 400)

        layout = QVBoxLayout()

        titolo = QLabel("Sono stati rilevati errori:")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
        layout.addWidget(titolo)

        # Area testo con errori
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setText(error_text)
        layout.addWidget(text_area)

        # Pulsante chiudi
        btn_close = QPushButton("Chiudi")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

        self.setLayout(layout)
