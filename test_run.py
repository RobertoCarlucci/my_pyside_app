import sys, traceback

sys.path.insert(0, r"C:\GitDb\my_pyside_app\src")
try:
    import pandas
    from PySide6.QtWidgets import QApplication
    from ui.main_qt import MainWindow

    print("IMPORT OK - avvio finestra...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("FINESTRA APERTA")
    # Non avvio il loop, chiudo subito
    sys.exit(0)
except Exception:
    traceback.print_exc()
    sys.exit(1)
