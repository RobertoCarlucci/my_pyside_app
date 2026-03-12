BUTTON_STYLES = {
    "primary": {
        "bg": "#0078D4",
        "fg": "white",
        "hover": "#005A9E",
        "font_size": 14,
        "radius": 6,
        "padding": "8px 16px",
    },
    "danger": {
        "bg": "#D83B01",
        "fg": "white",
        "hover": "#A52600",
        "font_size": 14,
        "radius": 6,
        "padding": "8px 16px",
    },
    "warning": {
        "bg": "#FFB900",
        "fg": "black",
        "hover": "#E0A000",
        "font_size": 14,
        "radius": 6,
        "padding": "8px 16px",
    },
    "flat": {
        "bg": "transparent",
        "fg": "#333",
        "hover": "#DDD",
        "font_size": 13,
        "radius": 4,
        "padding": "4px 8px",
    },
}

from PySide6.QtWidgets import QPushButton


def apply_button_style(button: QPushButton, style_name: str):
    if style_name not in BUTTON_STYLES:
        return

    s = BUTTON_STYLES[style_name]

    button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: {s['bg']};
            color: {s['fg']};
            border-radius: {s['radius']}px;
            padding: {s['padding']};
            font-size: {s['font_size']}px;
        }}
        QPushButton:hover {{
            background-color: {s['hover']};
        }}
    """
    )
