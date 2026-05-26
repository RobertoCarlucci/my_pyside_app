from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QStyle,
    QToolButton,
    QWidget,
)


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet("CustomTitleBar { background-color: #A8FF0E; }")
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setStyleSheet("""QLabel {
                   font-weight: bold;
                   color: #741B7C;
                   border: 2px solid #FFFFFF;
                   border-radius: 12px;
                   margin: 2px;
                }
            """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)

        # Min button
        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMinButton,
        )
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMaxButton,
        )
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window()._on_maximize)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarNormalButton
        )
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window()._on_restore)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 28))
            button.setStyleSheet("""QToolButton {
                        border: 2px solid white;
                        border-radius: 12px;
                    }
                """)
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state & Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
