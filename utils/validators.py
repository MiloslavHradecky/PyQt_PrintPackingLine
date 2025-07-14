from core.logger import Logger
from core.messenger import Messenger


class Validator:
    def __init__(self, print_window):
        self.print_window = print_window
        self.messenger = Messenger(parent=self.print_window)

        # 📝 Logging setup / Nastavení loggeru
        self.normal_logger = Logger(spaced=False)
        self.spaced_logger = Logger(spaced=True)

    def validate_input_exists_for_product(self, lbl_lines: list[str], serial: str) -> bool:
        """
        Validates that all key lines for a given serial number exist in lbl_lines.
        Ověří, že existují řádky SERIAL+B=, D=, E= pro daný serial number.

        :param lbl_lines: Seznam řádků z .lbl souboru
        :param serial: Zadaný serial number
        :return: True pokud všechny existují, jinak False + zobrazí warning
        """
        keys = [f'{serial}B=', f'{serial}D=', f'{serial}E=']
        missing_keys = [key for key in keys if not any(line.startswith(key) for line in lbl_lines)]

        if missing_keys:
            joined = ', '.join(missing_keys)
            self.normal_logger.log('Warning', f'Nebyly nalezeny všechny klíčové řádky: {joined}', 'VALIDAT001')
            self.messenger.show_warning('Warning', f'Některé klíčové řádky chybí: {joined}', 'VALIDAT001')
            self.reset_input_focus()
            return False

        return True
