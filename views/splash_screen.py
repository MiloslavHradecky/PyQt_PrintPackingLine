from PyQt6.QtWidgets import QSplashScreen, QLabel
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from pathlib import Path


class SplashScreen(QSplashScreen):
    def __init__(self, duration_ms=5000):
        base_dir = Path(__file__).parent.parent
        ico_dir = base_dir / 'resources' / 'ico'
        logo_path = ico_dir / 'splash_logo.png'
        spinner_path = ico_dir / 'spinner.gif'
        pixmap = QPixmap(str(logo_path)).scaled(1200, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.0)
        self.duration = duration_ms

        # 📝 Text
        self.label = QLabel("Načítání aplikace…", self)
        self.label.setStyleSheet("color: white; font-size: 36px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._resize_label()

        # 🌀 Spinner (GIF animace)
        self.spinner = QLabel(self)
        movie = QMovie(str(spinner_path))
        self.spinner.setMovie(movie)
        movie.start()
        self.spinner.setFixedSize(128, 128)
        self.spinner.setScaledContents(True)
        self.spinner.setGeometry(self.width() // 2 - 64, self.height() - 200, 128, 128)  # pozice spinneru

    def _resize_label(self):
        width = self.pixmap().width() or 300
        height = self.pixmap().height() or 200
        self.label.setGeometry(0, height - 100, width, 50)

    def start(self, on_finish_callback):
        self.show()
        self._animate_fade_in()
        QTimer.singleShot(self.duration, lambda: self._finish(on_finish_callback))

    def _animate_fade_in(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(0.9)
        self.animation.start()

    def _finish(self, callback):
        self.close()
        callback()
