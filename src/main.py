import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
