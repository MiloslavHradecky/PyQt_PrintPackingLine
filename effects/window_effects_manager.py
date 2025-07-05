# ✨ WindowEffectsManager – handles fade-in and fade-out animations
# Správce efektů přechodu oken (fade in / fade out) pro plynulou uživatelskou zkušenost

from PyQt6.QtCore import QPropertyAnimation


class WindowEffectsManager:
    def __init__(self):
        """
        Initializes the animation manager and internal storage.
        Inicializuje správce animací a vnitřní úložiště animací.
        """
        self._animations = {}

    def fade_in(self, widget, duration=3000):
        """
        Applies a fade-in effect to the window.
        Aplikuje efekt „zobrazení“ – plynulé zobrazení okna.

        :param widget: Target widget / Cílové okno
        :param duration: Duration in milliseconds / Délka trvání animace v ms
        """
        if widget in self._animations:
            self._animations[widget].stop()

        widget.setWindowOpacity(0.0)
        widget.show()
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.start()
        self._animations[widget] = animation  # ochrání před GC

    def fade_out(self, widget, duration=2000):
        """
        Applies a fade-out effect and closes the window when complete.
        Aplikuje efekt „zmizení“ a poté zavře okno.

        :param widget: Target widget / Cílové okno
        :param duration: Duration in milliseconds / Délka trvání animace v ms
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.start()
        animation.finished.connect(widget.close)
        self._animations[widget] = animation
