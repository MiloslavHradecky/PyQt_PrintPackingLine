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
            self.normal_logger.log('Error', f'Nebyly nalezeny všechny klíčové řádky: {joined}', 'VALIDATOR001')
            self.messenger.show_error('Error', f'Některé klíčové řádky v souboru .lbl chybí!', 'VALIDATOR001', False)
            self.print_window.reset_input_focus()
            return False

        return True

    def validate_injection_balice(self, header_fields: list[str], record_fields: list[str]) -> int | None:
        """
        Validates and returns index of 'P Znacka balice' in header_fields.
        Zkontroluje přítomnost pole a jeho indexaci vůči record_fields.

        :return: Validní index nebo None pokud není bezpečné provést injekci
        """
        try:
            index = header_fields.index('P Znacka balice')
            if index >= len(record_fields):
                self.normal_logger.log('Error', f'Neplatný index pole "P Znacka balice" v record.', 'VALIDATOR002')
                self.messenger.show_error('Error', f'Neplatný index pole "P Znacka balice".', 'VALIDATOR002', False)
                self.print_window.reset_input_focus()
                return None
            return index
        except ValueError:
            self.normal_logger.log('Error', f'Pole "P Znacka balice" nebylo nalezeno v hlavičce.', 'VALIDATOR003')
            self.messenger.show_error('Error', f'Pole "P Znacka balice" chybí.', 'VALIDATOR003', False)
            self.print_window.reset_input_focus()
            return None
