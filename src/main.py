import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

from PySide6.QtWidgets import QApplication
from main_win import MainWindow
import sys
import signal

if __name__ == "__main__":
    # Ripristina il comportamento standard di Ctrl+C (Qt lo sovrascrive)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
