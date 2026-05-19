from pathlib import Path
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

# Radice del pacchetto src/ (background_style.py si trova in src/ui/style/)
_SRC_DIR = Path(__file__).resolve().parent.parent.parent

BACKGROUND_STYLES = {
    "default": {"image": "assets/backgrounds/wallpaper_dl.png", "opacity": 0.65},
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
    bg.setScaledContents(False)
    bg._src_pixmap = faded  # type: ignore[attr-defined]
    bg.lower()  # mantiene lo sfondo sotto tutti gli altri widget
    bg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    resize_background(widget, bg)  # applica subito il cover centrato
    return bg


def resize_background(widget: QWidget, bg: QLabel) -> None:
    """
    Scala e centra la QLabel di sfondo in modalità cover rispetto a widget.
    Da chiamare nel resizeEvent della finestra.
    """
    src = getattr(bg, "_src_pixmap", None)
    if src is None:
        return
    scaled = src.scaled(
        widget.size(),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    x = (widget.width() - scaled.width()) // 2
    y = (widget.height() - scaled.height()) // 2
    bg.setPixmap(scaled)
    bg.setGeometry(x, y, scaled.width(), scaled.height())


def set_background_style(style_name: str, image: str, opacity: float = 1.0) -> None:
    """
    Aggiunge o aggiorna una voce in BACKGROUND_STYLES.
    style_name: chiave dello stile (es. "default", "dark", "custom")
    image:      percorso relativo a src/ dell'immagine
    opacity:    valore tra 0.0 e 1.0
    """
    BACKGROUND_STYLES[style_name] = {
        "image": image,
        "opacity": max(0.0, min(1.0, opacity)),
    }


def apply_background_style(widget: QWidget, style_name: str) -> QLabel | None:
    if style_name not in BACKGROUND_STYLES:
        print(f"⚠️ Stile sfondo non trovato: {style_name}")
        return None
    s = BACKGROUND_STYLES[style_name]
    return apply_background(widget, s["image"], s["opacity"])
