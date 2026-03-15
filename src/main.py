import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from db.database import init_db
import sys
import signal

if __name__ == "__main__":
    # Ripristina il comportamento standard di Ctrl+C (Qt lo sovrascrive)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
