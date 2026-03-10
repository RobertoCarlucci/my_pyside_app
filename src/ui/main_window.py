from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Imposta dimensione iniziale della finestra
        self.resize(600, 400)

        self.setWindowTitle("Template PySide6")

        # Imposta colore di sfondo (verde chiaro)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ccffcc"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout
        layout = QVBoxLayout()

        # Label centrata, corpo 8, colore rosso
        self.label = QLabel("Benvenuto nella tua app PySide6!")
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)

        self.label.setStyleSheet("color: red;")

        # Pulsante
        button = QPushButton("Cliccami")
        button.clicked.connect(self.on_click)

        layout.addWidget(self.label)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_click(self):
        self.label.setText("Hai cliccato il pulsante!")
