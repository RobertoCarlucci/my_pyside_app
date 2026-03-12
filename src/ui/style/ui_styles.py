UI_STYLES = {
    # ---------------------------------------------------------
    # QLabel
    # ---------------------------------------------------------
    "label_default": {"font_size": 13, "color": "#333", "bold": False},
    "label_title": {"font_size": 18, "color": "#222", "bold": True},
    "label_error": {"font_size": 14, "color": "red", "bold": True},
    # ---------------------------------------------------------
    # QLineEdit
    # ---------------------------------------------------------
    "lineedit_default": {
        "bg": "white",
        "fg": "#333",
        "border": "1px solid #CCC",
        "radius": 4,
        "padding": "4px",
    },
    "lineedit_error": {
        "bg": "#FFF0F0",
        "fg": "#900",
        "border": "1px solid #D00",
        "radius": 4,
        "padding": "4px",
    },
    # ---------------------------------------------------------
    # QComboBox
    # ---------------------------------------------------------
    "combobox_default": {
        "bg": "white",
        "fg": "#333",
        "border": "1px solid #CCC",
        "radius": 4,
        "padding": "4px",
    },
    # ---------------------------------------------------------
    # QFrame
    # ---------------------------------------------------------
    "frame_default": {"bg": "#F7F7F7", "border": "1px solid #DDD", "radius": 6},
    # ---------------------------------------------------------
    # QDialog
    # ---------------------------------------------------------
    "dialog_default": {"bg": "white", "border": "1px solid #AAA", "radius": 8},
    # ---------------------------------------------------------
    # QTableWidget
    # ---------------------------------------------------------
    "table_default": {
        "header_bg": "#EDEDED",
        "header_fg": "#333",
        "row_bg": "white",
        "row_alt_bg": "#FAFAFA",
        "grid_color": "#DDD",
        "font_size": 13,
    },
}

from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QComboBox,
    QFrame,
    QDialog,
    QTableWidget,
)


def apply_label_style(label: QLabel, style_name: str):
    s = UI_STYLES[style_name]
    weight = "bold" if s.get("bold") else "normal"

    label.setStyleSheet(
        f"""
        QLabel {{
            color: {s['color']};
            font-size: {s['font_size']}px;
            font-weight: {weight};
        }}
    """
    )


def apply_lineedit_style(le: QLineEdit, style_name: str):
    s = UI_STYLES[style_name]

    le.setStyleSheet(
        f"""
        QLineEdit {{
            background-color: {s['bg']};
            color: {s['fg']};
            border: {s['border']};
            border-radius: {s['radius']}px;
            padding: {s['padding']};
        }}
    """
    )


def apply_combobox_style(cb: QComboBox, style_name: str):
    s = UI_STYLES[style_name]

    cb.setStyleSheet(
        f"""
        QComboBox {{
            background-color: {s['bg']};
            color: {s['fg']};
            border: {s['border']};
            border-radius: {s['radius']}px;
            padding: {s['padding']};
        }}
    """
    )


def apply_frame_style(frame: QFrame, style_name: str):
    s = UI_STYLES[style_name]

    frame.setStyleSheet(
        f"""
        QFrame {{
            background-color: {s['bg']};
            border: {s['border']};
            border-radius: {s['radius']}px;
        }}
    """
    )


def apply_dialog_style(dialog: QDialog, style_name: str):
    s = UI_STYLES[style_name]

    dialog.setStyleSheet(
        f"""
        QDialog {{
            background-color: {s['bg']};
            border: {s['border']};
            border-radius: {s['radius']}px;
        }}
    """
    )


def apply_table_style(table: QTableWidget, style_name: str):
    s = UI_STYLES[style_name]

    table.setStyleSheet(
        f"""
        QTableWidget {{
            gridline-color: {s['grid_color']};
            font-size: {s['font_size']}px;
        }}
        QHeaderView::section {{
            background-color: {s['header_bg']};
            color: {s['header_fg']};
            padding: 4px;
            border: 1px solid #CCC;
        }}
    """
    )

    table.setAlternatingRowColors(True)
    table.setStyleSheet(
        table.styleSheet()
        + f"""
        QTableWidget::item:alternate {{
            background-color: {s['row_alt_bg']};
        }}
    """
    )
