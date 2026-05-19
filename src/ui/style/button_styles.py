BUTTON_STYLES = {
    "primary": {
        "bg": "#0078D4",
        "fg": "white",
        "hover": "#005A9E",
        "border_color": "#FFFFFF",  # Primary
        "border_width": 4,
        "font_size": 14,
        "radius": 20,
        "padding": "8px 16px",
        "height": 50,
        "shadow": True,
    },
    "secondary": {
        "bg": "#6C757D",
        "fg": "#FFB900",  # Yellow = #FFB900
        "hover": "#545B62",
        "border_color": "#FFB900",  # Primary
        "border_width": 4,
        "font_size": 14,
        "radius": 20,
        "padding": "8px 16px",
        "height": 50,
        "shadow": True,
    },
    "flat": {
        "bg": "transparent",
        "fg": "#333",
        "hover": "#DDD",
        "font_size": 13,
        "radius": 4,
        "padding": "4px 8px",
    },
    "warning": {
        "bg": "#FFB900",
        "fg": "#000000",  # Dark = Black
        "hover": "#E0A000",  # YellowGreen scurito
        "border_color": "#FFFFFF",  # Primary
        "border_width": 4,
        "font_size": 14,
        "radius": 20,
        "padding": "8px 16px",
        "height": 50,
        "shadow": True,
    },
    "danger": {
        "bg": "#D83B01",  # Rosso = Red
        "fg": "#FFFFFF",  # Dark = Black
        "hover": "#A52600",  # YellowGreen scurito
        "border_color": "#FFFFFF",  # Primary
        "border_width": 4,
        "font_size": 14,
        "radius": 20,
        "padding": "8px 16px",
        "height": 50,
        "shadow": True,
    },
    "my_button": {
        "bg": "#9ACD32",  # GialloVerde = YellowGreen
        "fg": "#000000",  # Dark = Black
        "hover": "#7BA428",  # YellowGreen scurito
        "border_color": "#FFC107",  # Primary
        "border_width": 4,
        "font_size": 14,
        "radius": 20,
        "padding": "8px 16px",
        "height": 50,
        "shadow": True,
    },
}

from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


def apply_button_style(button: QPushButton, style_name: str):
    if style_name not in BUTTON_STYLES:
        print(
            f"⚠️ Stile pulsante non trovato: '{style_name}'. Applicato stile 'primary' come default."
        )
        style_name = "primary"

    s = BUTTON_STYLES[style_name]

    border_color = s.get("border_color", "transparent")
    border_width = s.get("border_width", 0)
    border_line = f"{border_width}px solid {border_color}" if border_width else "none"

    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {s['bg']};
            color: {s['fg']};
            border-radius: {s['radius']}px;
            border: {border_line};
            padding: {s['padding']};
            font-size: {s['font_size']}px;
        }}
        QPushButton:hover {{
            background-color: {s['hover']};
        }}
        QPushButton:disabled {{
            background-color: #2A2A2A;
            color: #606060;
            border: 1px solid #3D3D3D;
        }}
    """)

    if s.get("height"):
        button.setFixedHeight(s["height"])

    if s.get("shadow"):
        shadow = QGraphicsDropShadowEffect(button)
        shadow.setColor(QColor("black"))
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        button.setGraphicsEffect(shadow)
    else:
        shadow = QGraphicsDropShadowEffect(button)
        shadow.setColor(QColor(0, 0, 0, 60))  # nero semi-trasparente
        shadow.setBlurRadius(4)
        shadow.setOffset(1, 1)
        button.setGraphicsEffect(shadow)
