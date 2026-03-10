from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Template PySide6")

        layout = QVBoxLayout()

        self.label = QLabel("Benvenuto nella tua app PySide6!")
        button = QPushButton("Cliccami")

        button.clicked.connect(self.on_click)

        layout.addWidget(self.label)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_click(self):
        self.label.setText("Hai cliccato il pulsante!")
