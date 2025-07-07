# 🚀 SplashScreen – animated startup screen with logo, text and spinner
# Úvodní obrazovka aplikace s logem, textem a animací načítání

from PyQt6.QtWidgets import QSplashScreen, QLabel
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from pathlib import Path


class SplashScreen(QSplashScreen):
    def __init__(self, duration_ms=5000):
        """
        Initializes splash screen appearance and animation.
        Inicializuje splash screen, včetně vzhledu a animace.

        :param duration_ms: Duration before transition / Doba zobrazení v milisekundách
        """
        base_dir = Path(__file__).parent.parent
        ico_dir = base_dir / 'resources' / 'ico'
        logo_path = ico_dir / 'splash_logo.png'
        spinner_path = ico_dir / 'spinner.gif'

        # 🖼️ Display the main application logo / Zobrazení hlavního loga aplikace
        pixmap = QPixmap(str(logo_path)).scaled(1200, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.0)
        self.duration = duration_ms

        # 📝 Text label / Textový popisek
        self.label = QLabel('Načítání aplikace…', self)
        self.label.setStyleSheet('color: white; font-size: 36px;')
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._resize_label()

        # 🌀 GIF animation of spinner / Spinner (GIF animace)
        self.spinner = QLabel(self)
        movie = QMovie(str(spinner_path))
        self.spinner.setMovie(movie)
        movie.start()
        self.spinner.setFixedSize(128, 128)
        self.spinner.setScaledContents(True)
        self.spinner.setGeometry(self.width() // 2 - 64, self.height() - 200, 128, 128)

    def _resize_label(self):
        """
        Positions the text label above the bottom edge.
        Umístí text nad spodní okraj splash okna.
        """
        width = self.pixmap().width() or 300
        height = self.pixmap().height() or 200
        self.label.setGeometry(0, height - 100, width, 50)

    def start(self, on_finish_callback):
        """
        Starts the splash screen animation and transition.
        Spustí splash obrazovku a naplánuje přechod po timeoutu.

        :param on_finish_callback: Function to call after timeout / Funkce po dokončení
        """
        self.show()
        self._animate_fade_in()
        QTimer.singleShot(self.duration, lambda: self._finish(on_finish_callback))

    def _animate_fade_in(self):
        """
        Applies fade-in opacity animation to the splash screen.
        Aplikuje animaci postupného zobrazení.
        """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(0.9)
        self.animation.start()

    def _finish(self, callback):
        """
        Closes splash screen and continues to next screen.
        Zavře splash screen a pokračuje na další obrazovku.
        """
        self.close()
        callback()
