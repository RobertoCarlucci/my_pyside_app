from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPalette, QColor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Imposta dimensione iniziale della finestra
        self.resize(600, 400)  # Larghezza 600px, altezza 400px

        self.setWindowTitle("Template PySide6")

        # Imposta colore di sfondo (verde chiaro)
        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor("#ccffcc"))  # verde chiaro pastello
        # self.setPalette(palette)
        # self.setAutoFillBackground(True)

        # Layout e contenuti
        layout = QVBoxLayout()

        self.label = QLabel("Benvenuto nella tua app PySide6!")
        button = QPushButton("Cliccami")

        button.clicked.connect(self.on_click)

        layout.addWidget(self.label)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_click(self):
        self.label.setText("Hai cliccato il pulsante!")
