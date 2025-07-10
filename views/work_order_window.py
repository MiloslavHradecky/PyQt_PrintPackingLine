# 📋 WorkOrderWindow – User interface for scanning work order codes
# Uživatelské rozhraní pro zadání výrobního příkazu

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from effects.window_effects_manager import WindowEffectsManager


class WorkOrderWindow(QWidget):
    """
    UI window for entering a work order (e.g., barcode/ID).
    Okno pro zadání nebo skenování pracovního příkazu.
    """

    def __init__(self, controller=None):
        """
        Initializes window appearance and layout.
        Inicializuje vzhled a komponenty okna.
        """
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 📌 Title and dimensions / Název a velikost okna
        self.setWindowTitle('Work Order')
        self.setFixedSize(400, 500)

        self.effects = WindowEffectsManager()
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Icon and logo paths / Cesty k ikonám
        base_dir = Path(__file__).parent.parent
        ico_dir = base_dir / 'resources' / 'ico'
        work_order_icon_path = ico_dir / 'work_order_find.ico'
        work_order_logo = ico_dir / 'work_order_find.png'

        # 📌 App icon / Ikona aplikace
        self.setWindowIcon(QIcon(str(work_order_icon_path)))

        # 📌 Font settings / Definice fontů
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        input_font = QFont('Arial', 12, QFont.Weight.Bold)

        # 📌 Window background / Barva pozadí
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D8E9F3'))
        self.setPalette(palette)

        # 📌 Main window layout / Hlavní layout okna
        layout = QVBoxLayout()

        # 📌 Application logo / Logo aplikace
        self.logo = QLabel(self)
        pixmap = QPixmap(str(work_order_logo)).scaled(self.width() - 20, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # 📌 Work order input field / Vstupní pole pro příkaz
        self.work_order_input: QLineEdit = QLineEdit()
        self.work_order_input.setFont(input_font)
        self.work_order_input.setPlaceholderText('Naskenujte pracovní příkaz')
        self.work_order_input.setStyleSheet('background-color: white; padding: 5px; color: black; border-radius: 8px; border: 2px solid #FFC107;')

        # 📌 Placeholder color / Barva nápovědy
        self.palette = self.work_order_input.palette()
        self.placeholder_color = QColor('#757575')
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, self.placeholder_color)
        self.work_order_input.setPalette(self.palette)

        # 📌 Button style sheet / Styl pro tlačítka
        button_style = """
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover:!disabled {
                background-color: #165AB6;
            }
            QPushButton:pressed:!disabled {
                background-color: #0D3F7C;
                padding: 4px;
                border: 2px solid #0A3563;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #ECEFF1;
                border: none;
            }
            """

        # ⏭️ Continue button / Tlačítko Pokračuj
        self.next_button: QPushButton = QPushButton('Pokračuj')
        self.next_button.setFont(button_font)
        self.next_button.setStyleSheet(button_style)

        # ❌ Exit button / Tlačítko Ukončit
        self.exit_button: QPushButton = QPushButton('Ukončit')
        self.exit_button.setFont(button_font)
        self.exit_button.setStyleSheet(button_style)

        # 📌 Enter triggers continue / Enter aktivuje pokračování
        self.work_order_input.returnPressed.connect(self.next_button.click)

        # 📦 Add widgets to layout / Přidání prvků do hlavního layoutu
        layout.addWidget(self.work_order_input)
        layout.addWidget(self.next_button)
        layout.addWidget(self.exit_button)

        # 📌 Setting the window layout / Nastavení layoutu okna
        self.setLayout(layout)

        # ⬆️ Window priority and visual effect / Priorita oken a vizuální efekt
        self.activateWindow()
        self.raise_()
        self.work_order_input.setFocus()
        self.effects.fade_in(self, duration=1000)  # 🌟 Visual animation / Vizuální animace
