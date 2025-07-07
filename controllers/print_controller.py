# 🖨️ PrintController – handles logic for serial input, validation, and print action
# Řídí logiku vstupu serial number, validaci a spuštění tisku

import re
from pathlib import Path
from core.logger import Logger
from core.messenger import Messenger
from views.print_window import PrintWindow
from core.config_loader import ConfigLoader


class PrintController:
    def __init__(self, window_stack, order_code: str, product_name: str):
        """
        Initializes the print controller and connects signals.
        Inicializuje PrintController a napojí akce tlačítek.
        """
        self.window_stack = window_stack
        self.print_window = PrintWindow(order_code, product_name, controller=self)

        self.messenger = Messenger()

        # 📝 Logging setup / Nastavení loggeru
        self.normal_logger = Logger(spaced=False)
        self.spaced_logger = Logger(spaced=True)

        # 🔗 Button actions / Napojení tlačítek
        self.print_window.print_button.clicked.connect(self.print_button_click)
        self.print_window.exit_button.clicked.connect(self.handle_exit)

    def validate_serial_number_input(self) -> bool:
        """
        Validates the entered serial number against expected format.
        Ověří, zda zadaný serial number odpovídá formátu 00-0000-0000.

        :return: True if input is valid, else False
        """
        input_value = self.print_window.serial_number_input.text().strip().upper()

        pattern = r'^\d{2}-\d{4}-\d{4}$'
        if not re.fullmatch(pattern, input_value):
            self.messenger.show_info('Info', f'Serial number musí být ve formátu 00-0000-0000.')
            self.reset_input_focus()
            return False

        return True

    def load_lbl_for_control4(self):
        """
        Loads the .lbl file for Control4 based on order_code and config path.
        Načte .lbl soubor pro Control4 podle kódu příkazu a cesty z config.ini.

        :return: List of lines or empty list if not found / Seznam řádků nebo prázdný list
        """
        # 🎯 Získání cesty z config.ini
        config = ConfigLoader()
        orders_path = config.get_path('orders_path')

        if not orders_path:
            self.messenger.show_error('Error', 'Konfigurační cesta "orders_path" nebyla nalezena.', 'CTRL401')
            return []

        # 🧩 Sestavení cesty k .lbl souboru
        lbl_file = orders_path / f'{self.print_window.order_code}.lbl'

        if not lbl_file.exists():
            self.messenger.show_info('Warning', f'Soubor {lbl_file} neexistuje.', 'CTRL402')
            return []

        try:
            # 📄 Načtení obsahu souboru
            return lbl_file.read_text(encoding='utf-8').splitlines()
        except Exception as e:
            self.messenger.show_error('Error', str(e), 'CTRL403')
            return []

    def print_button_click(self):
        pass

    def reset_input_focus(self):
        """
        Clears the input field and sets focus back to it.
        Vymaže vstupní pole a nastaví znovu focus.
        """
        self.print_window.serial_number_input.clear()
        self.print_window.serial_number_input.setFocus()

    def handle_exit(self):
        """
        Closes PrintWindow and returns to the previous window.
        Zavře PrintWindow a vrátí se na předchozí okno ve stacku.
        """
        self.print_window.effects.fade_out(self.print_window, duration=2000)
