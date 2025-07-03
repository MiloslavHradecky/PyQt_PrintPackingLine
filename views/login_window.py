from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from effects.window_effects_manager import WindowEffectsManager


class LoginWindow(QWidget):
    """
    Třída představující přihlašovací okno aplikace.
    - Zobrazuje vstupní pole pro heslo (skrytý text)
    - Má tlačítko pro potvrzení přihlášení
    - Propojená s 'ControllerApp', která zpracovává přihlášení
    """

    def __init__(self, controller=None):
        """
        Inicializuje 'LoginWindow' a nastaví jeho vizuální vzhled.
        - Přijímá 'controller', který spravuje logiku přihlášení
        - Nastavuje ikonu okna
        - Definuje fonty, barvy a celkové UI rozvržení
        """
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 📌 Nastavení názvu a velikosti okna
        self.setWindowTitle('Přihlášení')
        self.setFixedSize(400, 500)

        self.effects = WindowEffectsManager()
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Nastavení ikony okna
        icon_login_path = Path('ico') / 'login.ico'
        self.setWindowIcon(QIcon(str(icon_login_path)))  # ✅ Ikona aplikace

        # 📌 Definice fontů pro UI prvky
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        input_font = QFont('Arial', 12, QFont.Weight.Bold)

        # 📌 Nastavení barvy pozadí okna
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D8E9F3'))  # ✅ Světle modrá barva pozadí
        self.setPalette(palette)

        # 📌 Hlavní layout okna
        layout = QVBoxLayout()

        # 📌 Logo aplikace
        login_logo = Path('ico') / 'login.tiff'
        self.logo = QLabel(self)
        pixmap = QPixmap(str(login_logo)).scaled(self.width() - 20, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # 📌 Pole pro zadání hesla (ID karta)
        self.input_password: QLineEdit = QLineEdit()
        self.input_password.setFont(input_font)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)  # ✅ Skryté zadávání hesla
        self.input_password.setPlaceholderText('Naskenujte svoji ID kartu')
        self.input_password.setStyleSheet('background-color: white; padding: 5px; color: black; border-radius: 8px; border: 2px solid #FFC107;')

        # 📌 Nastavení barvy textu pro placeholder
        self.palette = self.input_password.palette()
        self.placeholder_color = QColor('#757575')  # ✅ Šedá barva pro placeholder text
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, self.placeholder_color)
        self.input_password.setPalette(self.palette)

        # 📌 Nastavení barvy tlačítek
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

        # 📌 Tlačítko pro přihlášení
        self.login_button: QPushButton = QPushButton('Přihlásit se')
        self.login_button.setFont(button_font)
        self.login_button.setStyleSheet(button_style)

        # 📌 Tlačítko pro výběr 'Ukončit'
        self.exit_button: QPushButton = QPushButton('Ukončit')
        self.exit_button.setFont(button_font)
        self.exit_button.setStyleSheet(button_style)

        # 📌 Propojení tlačítka s akcí přihlášení
        self.input_password.returnPressed.connect(self.login_button.click)  # ✅ Enter aktivuje tlačítko

        # 📌 Přidání prvků do hlavního layoutu
        layout.addWidget(self.input_password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        # 📌 Nastavení layoutu okna
        self.setLayout(layout)

        self.activateWindow()  # ✅ Zajistíme, že okno získá prioritu
        self.raise_()  # ✅ Přivedeme okno do popředí

        self.input_password.setFocus()  # 🎯 automaticky umístí kurzor do pole
        self.effects.fade_in(self)  # 🌟 vizuální animace
