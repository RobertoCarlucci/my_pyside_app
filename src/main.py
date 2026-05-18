from App import *

if __name__ == "__main__":
    # Necessario per evitare crash QMutex nel runner di VS Code
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

    # Ripristina il comportamento standard di Ctrl+C (Qt lo sovrascrive)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
