import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

import sys
import signal
import os

# Forza il debugger pydevd a tracciare correttamente gli eventi PySide6
os.environ["PYDEVD_PYQT_MODE"] = "pyside6"

# Se necessario, forza l'inizializzazione del tracciamento delle funzioni
sys.settrace(sys.gettrace())

from main_win import MainWindow

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Assicura che la cartella src sia nel path e sia la cwd,
# indipendentemente da dove viene lanciato lo script.
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)
os.chdir(_SRC_DIR)

# Percorso del file DB (nella cartella principale del progetto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "app.db")

if __name__ == "__main__":
    # Necessario per evitare crash QMutex nel runner di VS Code
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

    # Ripristina il comportamento standard di Ctrl+C (Qt lo sovrascrive)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
