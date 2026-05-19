import pandas  # deve essere importato prima di PySide6 per evitare conflitti con shibokensupport/six

import sys
import signal
import os

from main_win import MainWindow

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QDialog,
    QTextEdit,
    QVBoxLayout,
)

from PySide6.QtGui import QFont, QPixmap, QPainter
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
