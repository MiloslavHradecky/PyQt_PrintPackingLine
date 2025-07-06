# 🖨️ PrintController – handles logic for serial input, validation, and print action
# Řídí logiku vstupu serial number, validaci a spuštění tisku

import re
from pathlib import Path
from core.logger import Logger
from core.messenger import Messenger
from views.print_window import PrintWindow


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
        input_value = self.print_window.serial_number_input.text().strip()

        pattern = r'^\d{2}-\d{4}-\d{4}$'
        if not re.fullmatch(pattern, input_value):
            self.messenger.show_info('Info', f'Serial number musí být ve formátu 00-0000-0000.')
            self.reset_input_focus()
            return False

        return True

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
