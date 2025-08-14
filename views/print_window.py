# 🖨️ PrintWindow – UI for serial number input and print action
# Uživatelské rozhraní pro zadání výrobního čísla a tisk

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from effects.window_effects_manager import WindowEffectsManager


class PrintWindow(QWidget):
    """
    Displays information about the work order and product and allows printing.
    Zobrazuje informace o příkazu a produktu a umožňuje pokračovat tiskem.
    """

    def __init__(self, order_code: str, product_name: str, controller=None):
        """
        Initializes the PrintWindow and prepares UI.
        Inicializuje tiskové okno a připraví rozhraní.

        :param order_code: Code of the active work order / Kód výrobního příkazu
        :param product_name: Human-readable product name / Název produktu
        :param controller: Optional controlling logic class
        """
        super().__init__()

        self.order_code = order_code
        self.product_name = product_name
        self.controller = controller

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 🪟 Title and size / Název a rozměry okna
        self.setWindowTitle('Print Line B')
        self.setFixedSize(400, 500)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.effects = WindowEffectsManager()

        # 📁 Load icon paths / Načti cesty k ikonám
        base_dir = Path(__file__).parent.parent
        ico_dir = base_dir / 'resources' / 'ico'
        icon_print_path = ico_dir / 'print.ico'
        print_logo = ico_dir / 'print.png'
        self.setWindowIcon(QIcon(str(icon_print_path)))

        # 🔠 Fonts / Definice fontů
        label_font = QFont('Arial', 11, QFont.Weight.Bold)
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        input_font = QFont('Arial', 12, QFont.Weight.Bold)

        # 🎨 Background color / Nastavení barvy pozadí okna
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D8E9F3'))
        self.setPalette(palette)

        # 🧱 Layout definition / Hlavní layout okna
        layout = QVBoxLayout()

        # 📌 Dynamic label with order and product / Dynamický popisek
        self.print_label = QLabel(f'<span style="color: black;">Příkaz:&nbsp;<b><span style="color:#C0392B">{self.order_code}</span></b>&nbsp;&nbsp;&nbsp;<span style="color: black;">Produkt:&nbsp;<b><span style="color:#C0392B">{self.product_name}</span></b>')
        self.print_label.setFont(label_font)
        self.print_label.setFixedHeight(32)
        self.print_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # 📌 Logo / Logo aplikace
        self.logo = QLabel(self)
        pixmap = QPixmap(str(print_logo)).scaled(self.width() - 20, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 📌 Serial number input / Vstupní pole pro serial number
        self.serial_number_input: QLineEdit = QLineEdit()
        self.serial_number_input.setFont(input_font)
        self.serial_number_input.setPlaceholderText('Naskenujte serial number')
        self.serial_number_input.setStyleSheet('background-color: white; padding: 5px; color: black; border-radius: 8px; border: 2px solid #FFC107;')

        # 📌 Placeholder color / Nastavení barvy textu pro placeholder
        self.palette = self.serial_number_input.palette()
        self.placeholder_color = QColor('#757575')
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, self.placeholder_color)
        self.serial_number_input.setPalette(self.palette)

        # 🔘 Button styles / Nastavení barvy tlačítek
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

        # 🖨️ Print button / Tlačítko pro přihlášení
        self.print_button: QPushButton = QPushButton('Tisk')
        self.print_button.setFont(button_font)
        self.print_button.setStyleSheet(button_style)

        # ❌ Back button / Tlačítko pro výběr 'Zpět'
        self.exit_button: QPushButton = QPushButton('Zpět')
        self.exit_button.setFont(button_font)
        self.exit_button.setStyleSheet(button_style)

        # 📌 Enter triggers print / Propojení tlačítka s akcí přihlášení
        self.serial_number_input.returnPressed.connect(self.print_button.click)

        # 📌 Add elements to the main layout / Přidání prvků do hlavního layoutu
        layout.addWidget(self.print_label)
        layout.addWidget(self.logo)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.print_button)
        layout.addWidget(self.exit_button)

        # 📦 Finalize layout / Nastavení layoutu okna
        self.setLayout(layout)
        self.activateWindow()
        self.raise_()
        self.serial_number_input.setFocus()

        # ✨ Launch animation / Vizuální animace
        self.effects.fade_in(self, duration=1000)

    def reset_input_focus(self):
        """
        Clears the input field and sets focus back to it.
        Vymaže vstupní pole a nastaví znovu focus.
        """
        self.serial_number_input.clear()
        self.serial_number_input.setFocus()
