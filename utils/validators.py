from core.logger import Logger
from core.messenger import Messenger
from utils.szv_utils import get_value_prefix


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
            self.normal_logger.log('Error', f'Nebyly nalezeny všechny klíčové řádky: {joined}', 'VALIDATOR001')
            self.messenger.show_error('Error', f'Některé klíčové řádky v souboru .lbl chybí!', 'VALIDATOR001', False)
            self.print_window.reset_input_focus()
            return False

        return True

    def validate_and_inject_balice(self, header: str, record: str) -> str | None:
        """
        Validates and injects prefix to 'P Znacka balice' field.
        Zkontroluje správnost, provede injekci do record, nebo vrátí None při chybě.
        """
        header_fields = header.split('","')
        record_fields = record.split('","')

        try:
            index = header_fields.index('P Znacka balice')
            if index >= len(record_fields):
                self.normal_logger.log('Error', 'Neplatný index pole "P Znacka balice"', 'VALIDATOR002')
                self.messenger.show_error('Error', 'Neplatný index pole v record.', 'VALIDATOR002', False)
                self.print_window.reset_input_focus()
                return None

            prefix = get_value_prefix()
            record_fields[index] = prefix
            return '","'.join(record_fields)

        except ValueError:
            self.normal_logger.log('Error', 'Pole "P Znacka balice" chybí.', 'VALIDATOR003')
            self.messenger.show_error('Error', 'Pole v header nebylo nalezeno.', 'VALIDATOR003', False)
            self.print_window.reset_input_focus()
            return None
