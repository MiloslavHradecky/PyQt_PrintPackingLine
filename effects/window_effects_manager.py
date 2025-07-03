from PyQt6.QtCore import QPropertyAnimation


class WindowEffectsManager:
    def __init__(self):
        self._animations = {}

    def fade_in(self, widget, duration=700):
        widget.setWindowOpacity(0.0)
        widget.show()
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.start()
        self._animations[widget] = animation  # ochrání před GC

    def fade_out(self, widget, duration=700):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.start()
        animation.finished.connect(widget.close)
        self._animations[widget] = animation
