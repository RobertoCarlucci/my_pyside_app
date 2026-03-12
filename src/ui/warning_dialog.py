from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class WarningDialog(QDialog):

    def __init__(self, warning_text: str):
        super().__init__()

        self.setWindowTitle("Warning durante l'importazione")
        self.resize(600, 400)

        layout = QVBoxLayout()

        titolo = QLabel("Sono stati rilevati dei warning:")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 16px; font-weight: bold; color: orange;")
        layout.addWidget(titolo)

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setText(warning_text)
        layout.addWidget(text_area)

        # Pulsanti
        buttons = QHBoxLayout()

        btn_cancel = QPushButton("Annulla")
        btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(btn_cancel)

        btn_continue = QPushButton("Continua comunque")
        btn_continue.clicked.connect(self.accept)
        buttons.addWidget(btn_continue)

        layout.addLayout(buttons)

        self.setLayout(layout)
