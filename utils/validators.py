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

    def extract_header_and_record(self, lbl_lines: list[str], serial: str) -> tuple[str, str] | None:
        key_d = f'{serial}D='
        key_e = f'{serial}E='
        header = None
        record = None

        for line in lbl_lines:
            if line.startswith(key_d):
                header = line.split('D=')[1].strip()
            elif line.startswith(key_e):
                record = line.split('E=')[1].strip()

        if not header or not record:
            self.normal_logger.log('Error', f'Nebyly nalezeny hlavička nebo záznam pro "{serial}".', 'VALIDATOR004')
            self.messenger.show_error('Error', f'Nebyly nalezeny hlavička nebo záznam pro "{serial}".', 'VALIDATOR004', False)
            self.print_window.reset_input_focus()
            return None

        return header, record

    def extract_trigger_values(self, lbl_lines: list[str], serial: str) -> list[str] | None:
        key_b = f'{serial}B='
        for line in lbl_lines:
            if line.startswith(key_b):
                raw_value = line.split('B=')[1]
                values = [val.strip() for val in raw_value.split(';') if val.strip()]
                return values

        self.normal_logger.log('Error', f'Řádek \"{key_b}\" nebyl nalezen.', 'VALIDATOR005')
        self.messenger.show_error('Error', f'Řádek \"{key_b}\" nebyl nalezen.', 'VALIDATOR005', False)
        self.print_window.reset_input_focus()
        return None

    def extract_header_and_record_c4(self, lbl_lines: list[str], serial: str) -> tuple[str, str] | None:
        key_j = f'{serial}J='
        key_k = f'{serial}K='
        header = None
        record = None

        for line in lbl_lines:
            if line.startswith(key_j):
                header = line.split('J=')[1].strip()
            elif line.startswith(key_k):
                record = line.split('K=')[1].strip()

        if not header or not record:
            self.normal_logger.log('Error', f'Nebyly nalezeny J/K řádky pro serial "{serial}".', 'VALIDATOR006')
            self.messenger.show_error('Error', f'Nebyly nalezeny J/K řádky pro serial "{serial}".', 'VALIDATOR006', False)
            self.print_window.reset_input_focus()
            return None

        return header, record

    def extract_trigger_values_c4(self, lbl_lines: list[str], serial: str) -> list[str] | None:
        key_i = f'{serial}I='
        for line in lbl_lines:
            if line.startswith(key_i):
                raw_value = line.split('I=')[1]
                return [val.strip() for val in raw_value.split(';') if val.strip()]

        self.normal_logger.log('Error', f'Řádek \"{key_i}\" nebyl nalezen.', 'VALIDATOR007')
        self.messenger.show_error('Error', f'Řádek \"{key_i}\" nebyl nalezen.', 'VALIDATOR007', False)
        self.print_window.reset_input_focus()
        return None

    def validate_input_exists_for_control4(self, lbl_lines: list[str], serial: str) -> bool:
        """
        Validates that all key lines for a given serial number exist in lbl_lines.
        Ověří, že existují řádky SERIAL+I=, J=, K= pro daný serial number.

        :param lbl_lines: Seznam řádků z .lbl souboru
        :param serial: Zadaný serial number
        :return: True pokud všechny existují, jinak False + zobrazí warning
        """
        keys = [f'{serial}I=', f'{serial}J=', f'{serial}K=']
        missing_keys = [key for key in keys if not any(line.startswith(key) for line in lbl_lines)]

        if missing_keys:
            joined = ', '.join(missing_keys)
            self.normal_logger.log('Error', f'Nebyly nalezeny všechny klíčové řádky: {joined}', 'VALIDATOR008')
            self.messenger.show_error('Error', f'Některé klíčové řádky v souboru .lbl chybí!', 'VALIDATOR008', False)
            self.print_window.reset_input_focus()
            return False

        return True