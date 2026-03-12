from pathlib import Path
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

# Radice del pacchetto src/ (background_style.py si trova in src/ui/style/)
_SRC_DIR = Path(__file__).resolve().parent.parent.parent

BACKGROUND_STYLES = {
    "default": {"image": "assets/backgrounds/wallpaper_dl.png", "opacity": 0.25},
    "dark": {"image": "assets/backgrounds/wallpaper_dl.png", "opacity": 0.40},
    "light": {"image": "assets/backgrounds/wallpaper_dl.png", "opacity": 0.15},
}


def apply_background(
    widget: QWidget, image_path: str, opacity: float = 1.0
) -> QLabel | None:
    """
    Crea una QLabel di sfondo che copre l'intero widget e si ridimensiona
    automaticamente tramite resizeEvent.
    image_path: percorso relativo a src/
    opacity: valore tra 0.0 e 1.0
    Restituisce la QLabel di sfondo (o None se l'immagine non è trovata).
    """
    opacity = max(0.0, min(1.0, opacity))
    abs_path = _SRC_DIR / image_path
    src_pixmap = QPixmap(str(abs_path))
    if src_pixmap.isNull():
        print(f"⚠️ Immagine non trovata: {abs_path}")
        return None

    # Applica l'opacità creando un pixmap traslucido
    faded = QPixmap(src_pixmap.size())
    faded.fill(Qt.GlobalColor.transparent)
    p = QPainter(faded)
    p.setOpacity(opacity)
    p.drawPixmap(0, 0, src_pixmap)
    p.end()

    bg = QLabel(widget)
    bg.setPixmap(faded)
    bg.setScaledContents(False)  # il rescaling viene fatto manualmente nel resizeEvent
    bg._src_pixmap = faded  # type: ignore[attr-defined]
    bg.setGeometry(widget.rect())
    bg.lower()  # mantiene lo sfondo sotto tutti gli altri widget
    bg.setAttribute(
        Qt.WidgetAttribute.WA_TransparentForMouseEvents
    )  # non cattura mouse
    return bg


def apply_background_style(widget: QWidget, style_name: str) -> QLabel | None:
    if style_name not in BACKGROUND_STYLES:
        print(f"⚠️ Stile sfondo non trovato: {style_name}")
        return None
    s = BACKGROUND_STYLES[style_name]
    return apply_background(widget, s["image"], s["opacity"])
