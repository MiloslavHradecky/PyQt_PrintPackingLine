# 🔐 LoginWindow – GUI login screen with password entry for ID card systems
# Přihlašovací okno aplikace s polem pro ID kartu a animovaným vzhledem

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from effects.window_effects_manager import WindowEffectsManager


class LoginWindow(QWidget):
    """
    Class representing the application login window.
    Třída představující přihlašovací okno aplikace.

    - Displays the password input field (hidden text)
    - Has a button to confirm the login
    - Linked to the ‘ControllerApp’ that processes the login
    """

    def __init__(self, controller=None):
        """
        Initializes the ‘LoginWindow’ and sets its visual appearance.
        Inicializuje 'LoginWindow' a nastaví jeho vizuální vzhled.

        - Receives a ‘controller’ that manages the login logic
        - Sets the icon of the window
        - Defines fonts, colors and overall UI layout
        """
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 📌 Setting the window name and size / Nastavení názvu a velikosti okna
        self.setWindowTitle('Přihlášení')
        self.setFixedSize(400, 500)

        self.effects = WindowEffectsManager()
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Paths to icons / Cesty k ikonám
        base_dir = Path(__file__).parent.parent
        ico_dir = base_dir / 'resources' / 'ico'

        icon_login_path = ico_dir / 'login.ico'
        login_logo = ico_dir / 'login.tiff'

        # 📌 Window icon settings / Nastavení ikony okna
        self.setWindowIcon(QIcon(str(icon_login_path)))

        # 📌 Defining fonts for UI elements / Definice fontů pro UI prvky
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        input_font = QFont('Arial', 12, QFont.Weight.Bold)

        # 📌 Setting the window background colour / Nastavení barvy pozadí okna
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D8E9F3'))
        self.setPalette(palette)

        # 📌 Main window layout / Hlavní layout okna
        layout = QVBoxLayout()

        # 📌 Application logo / Logo aplikace
        self.logo = QLabel(self)
        pixmap = QPixmap(str(login_logo)).scaled(self.width() - 20, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # 📌 Password field (ID card) / Pole pro zadání hesla (ID karta)
        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # 💡 Hidden password entry / Skryté zadávání hesla
        self.password_input.setPlaceholderText('Naskenujte svoji ID kartu')
        self.password_input.setStyleSheet('background-color: white; padding: 5px; color: black; border-radius: 8px; border: 2px solid #FFC107;')

        # 📌 Set text color for placeholder / Nastavení barvy textu pro placeholder
        self.palette = self.password_input.palette()
        self.placeholder_color = QColor('#757575')
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, self.placeholder_color)
        self.password_input.setPalette(self.palette)

        # 📌 Setting the colour of the buttons / Nastavení barvy tlačítek
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

        # 📌 Login button / Tlačítko pro přihlášení
        self.login_button: QPushButton = QPushButton('Přihlásit se')
        self.login_button.setFont(button_font)
        self.login_button.setStyleSheet(button_style)

        # 📌 Button to select 'Exit' / Tlačítko pro výběr 'Ukončit'
        self.exit_button: QPushButton = QPushButton('Ukončit')
        self.exit_button.setFont(button_font)
        self.exit_button.setStyleSheet(button_style)

        # 📌 Enter activates the button / Enter aktivuje tlačítko
        self.password_input.returnPressed.connect(self.login_button.click)

        # 📌 Adding elements to the main layout / Přidání prvků do hlavního layoutu
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        # 📌 Window layout settings / Nastavení layoutu okna
        self.setLayout(layout)

        self.activateWindow()  # 💡 We make sure that the window gets priority / Zajistíme, že okno získá prioritu
        self.raise_()  # 💡 Bring the window to the foreground / Přivedeme okno do popředí

        self.password_input.setFocus()
        self.effects.fade_in(self, duration=3000)  # 🌟 Visual animation / Vizuální animace
