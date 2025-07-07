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

    def load_file_lbl(self):
        """
        Loads the .lbl file based on order_code and config path.
        Načte .lbl soubor podle kódu příkazu a cesty z config.ini.

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
            return lbl_file.read_text().splitlines()
        except Exception as e:
            self.messenger.show_error('Error', str(e), 'CTRL403')
            return []

    def control4_save_and_print(self, lbl_lines: list[str]) -> None:
        """
        Extracts header and record for the scanned serial number and writes them to Control4 output file.
        Načte hlavičku a záznam z řádků .lbl pro naskenovaný serial number a zapíše je do výstupního souboru Control4.

        - Hledá řádky začínající na: SERIAL+I= a SERIAL+J= a SERIAL+K=
        - Pokud najde hlavičku i záznam, zapíše je do výstupního souboru

        :param lbl_lines: List of lines from .lbl file / Seznam řádků ze souboru
        """
        # 🧠 Získání vstupu ze scanu
        base_input = self.print_window.serial_number_input.text().strip().upper()
        key_i = f'{base_input}I='
        key_j = f'{base_input}J='
        key_k = f'{base_input}K='

        header = None
        record = None

        for line in lbl_lines:
            if line.startswith(key_j):
                header = line.split('J=')[1].strip()
            elif line.startswith(key_k):
                record = line.split('K=')[1].strip()

        # 🚦 Kontrola nálezů
        if not header or not record:
            self.messenger.show_warning('Warning', f'Není dostupná hlavička nebo data pro serial number "{base_input}".', 'CTRL405')
            return

        # 📁 Získání cesty z configu
        config = ConfigLoader()
        output_path = config.get_path('output_file_path_c4_product')

        if not output_path:
            self.messenger.show_error('Error', f'Cesta k výstupnímu souboru Control4 nebyla nalezena.', 'CTRL406')
            return

        try:
            # 💾 Zápis hlavičky + záznamu
            with output_path.open('w') as file:
                file.write(header + '\n')
                file.write(record + '\n')

            self.normal_logger.log('Info', f'Control4 záznam uložen.', 'CTRL407')

        except Exception as e:
            self.messenger.show_error('Error', f'Chyba zápisu {str(e)}', 'CTRL408')

    def print_button_click(self):
        if not self.validate_serial_number_input():
            return

        lbl_lines = self.load_file_lbl()
        if lbl_lines:
            self.control4_save_and_print(lbl_lines)

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
