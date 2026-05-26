from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QEvent, QTimer

from ui.style.background_style import apply_background_style, resize_background
from ui.style.titlebar_style import CustomTitleBar


class BasePage(QWidget):
    """
    Base class per tutte le finestre frameless dell'applicazione.

    Imposta automaticamente:
    - FramelessWindowHint
    - Sfondo personalizzato (via apply_background_style)
    - QVBoxLayout principale con CustomTitleBar in cima
    - self.content: QWidget trasparente su cui le sottoclassi aggiungono il proprio layout

    Propagazione stato finestra e resize sfondo gestiti qui.
    """

    def __init__(
        self,
        title: str,
        size: tuple = (960, 540),
        bg_style: str = "default",
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self._bg_label = None
        self.resize(*size)

        # Sfondo
        self._bg_label = apply_background_style(self, bg_style)

        # Layout principale: title bar + area contenuto
        _main = QVBoxLayout(self)
        _main.setContentsMargins(0, 0, 0, 0)
        _main.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.title_bar.setFixedHeight(32)
        _main.addWidget(self.title_bar)

        # Widget contenuto (trasparente): le sottoclassi ci aggiungono il proprio QGridLayout
        self.content = QWidget(self)
        self.content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        _main.addWidget(self.content)

        self._was_maximized = False

    # ------------------------------------------------------------------
    # Propagazione stato finestra → title bar (min/max/restore)
    # ------------------------------------------------------------------
    def _on_maximize(self):
        """Salva la geometria corrente e massimizza."""
        self._saved_geometry = self.geometry()
        self.showMaximized()

    def _on_restore(self):
        """Ripristina la geometria salvata prima del maximize.
        Gestisce il caso in cui Qt abbia perso traccia dello stato
        massimizzato (finestre frameless su Windows)."""
        self.showNormal()
        if self._saved_geometry:
            self.setGeometry(self._saved_geometry)
            self._saved_geometry = None
        self.title_bar.window_state_changed(Qt.WindowState.WindowNoState)

    def _sync_title_bar_on_show(self):
        """Chiamato da showEvent (ripristino dalla barra di Windows).
        Usa la geometria come fallback perché windowState() potrebbe
        non riflettere lo stato massimizzato per le finestre frameless."""
        is_max = bool(self.windowState() & Qt.WindowState.WindowMaximized)
        if not is_max and self.screen():
            wa = self.screen().availableGeometry()
            g = self.geometry()
            is_max = g.width() >= wa.width() and g.height() >= wa.height()
        state = Qt.WindowState.WindowMaximized if is_max else Qt.WindowState.WindowNoState
        self.title_bar.window_state_changed(state)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._sync_title_bar_on_show)

    # ------------------------------------------------------------------
    # Ridimensionamento sfondo
    # ------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._bg_label is not None:
            resize_background(self, self._bg_label)
