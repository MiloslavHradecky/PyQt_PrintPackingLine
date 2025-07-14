# 🖨️ PrintController – handles logic for serial input, validation, and print action
# Řídí logiku vstupu serial number, validaci a spuštění tisku

import re
from pathlib import Path
from core.logger import Logger
from core.messenger import Messenger
from views.print_window import PrintWindow
from core.config_loader import ConfigLoader
from utils.validators import Validator


class PrintController:
    """
    Main logic controller for print operations in the application.
    Hlavní řídicí třída pro tiskové operace v aplikaci.

    - Handles serial number validation, .lbl file parsing, and configuration-based output decisions
    - Manages dynamic printing for multiple product types based on config-defined mappings
    - Generates structured text files and trigger signals for label printing systems
    - Operates with PrintWindow GUI and connects button actions to appropriate processing

    - Řídí validaci sériových čísel, parsování .lbl souborů a rozhodování podle konfigurace
    - Obsluhuje dynamické tisky pro různé typy produktů dle mapování v config.ini
    - Generuje strukturované výstupní soubory i spouštěcí soubory pro tiskové systémy
    - Komunikuje s PrintWindow GUI a propojuje tlačítka s odpovídajícím zpracováním
    """

    def __init__(self, window_stack, order_code: str, product_name: str):
        """
        Initializes the print controller and connects signals.
        Inicializuje PrintController a napojí akce tlačítek.
        """
        self.window_stack = window_stack
        self.print_window = PrintWindow(order_code, product_name, controller=self)
        self.validator = Validator(self.print_window)

        self.messenger = Messenger(parent=self.print_window)
        self.config = ConfigLoader()

        # 📝 Logging setup / Nastavení loggeru
        self.normal_logger = Logger(spaced=False)
        self.spaced_logger = Logger(spaced=True)

        # 🔗 Button actions / Napojení tlačítek
        self.print_window.print_button.clicked.connect(self.print_button_click)
        self.print_window.exit_button.clicked.connect(self.handle_exit)

    @property
    def serial_input(self) -> str:
        """
        Returns cleaned serial number from input field.
        Vrací očištěný serial number ze vstupního pole.
        """
        return self.print_window.serial_number_input.text().strip().upper()

    @property
    def product_name(self) -> str:
        """
        Returns cleaned product name from print window.
        Vrací očištěný název produktu z print window.
        """
        return self.print_window.product_name.strip().upper()

    def get_trigger_dir(self) -> Path | None:
        """
        Returns trigger directory path from config.
        Vrací cestu ke složce trigger souborů z config.ini.
        """
        path = self.config.get_path('trigger_path', section='Paths')
        if path and path.exists():
            return path
        return None

    def validate_serial_number_input(self) -> bool:
        """
        Validates the entered serial number against expected format.
        Ověří, zda zadaný serial number odpovídá formátu 00-0000-0000.

        :return: True if input is valid, else False
        """
        input_value = self.serial_input

        pattern = r'^\d{2}-\d{4}-\d{4}$'
        if not re.fullmatch(pattern, input_value):
            self.messenger.show_info('Info', f'Serial number musí být ve formátu 00-0000-0000.')
            self.print_window.reset_input_focus()
            return False

        return True

    def load_file_lbl(self):
        """
        Loads the .lbl file based on order_code and config path.
        Načte .lbl soubor podle kódu příkazu a cesty z config.ini.

        :return: List of lines or empty list if not found / Seznam řádků nebo prázdný list
        """
        # 🎯 Getting path from config.ini / Získání cesty z config.ini
        orders_path = self.config.get_path('orders_path', section='Paths')

        if not orders_path:
            self.normal_logger.log('Error', f'Konfigurační cesta {orders_path} nebyla nalezena!', 'PRICON001')
            self.messenger.show_error('Error', f'Konfigurační cesta {orders_path} nebyla nalezena!', 'PRICON001', False)
            self.print_window.reset_input_focus()
            return []

        # 🧩 Build path to .lbl file / Sestavení cesty k .lbl souboru
        lbl_file = orders_path / f'{self.print_window.order_code}.lbl'

        if not lbl_file.exists():
            self.normal_logger.log('Warning', f'Soubor {lbl_file} neexistuje.', 'PRICON002')
            self.messenger.show_info('Warning', f'Soubor {lbl_file} neexistuje.', 'PRICON002')
            self.print_window.reset_input_focus()
            return []

        try:
            # 📄 Load the contents of a file / Načtení obsahu souboru
            return lbl_file.read_text().splitlines()
        except Exception as e:
            self.normal_logger.log('Error', f'Chyba načtení souboru {str(e)}', 'PRICON003')
            self.messenger.show_error('Error', f'{str(e)}', 'PRICON003', False)
            self.print_window.reset_input_focus()
            return []

    def control4_save_and_print(self, header: str, record: str, trigger_values: list[str]) -> None:
        """
        Extracts header and record for the scanned serial number and writes them to Control4 output file.
        Načte hlavičku a záznam z řádků .lbl pro naskenovaný serial number a zapíše je do výstupního souboru Control4.

        - Hledá řádky začínající na: SERIAL+I= a SERIAL+J= a SERIAL+K=
        - Pokud najde hlavičku i záznam, zapíše je do výstupního souboru

        :param header: extracted header line / extrahovaná hlavička z .lbl
        :param record: extracted record line / extrahovaný záznam z .lbl
        :param trigger_values: list of trigger filenames / seznam názvů souborů spouštěče
        """
        # 📁 Retrieve output file path from config / Získání cesty k výstupnímu souboru z konfigurace
        output_path = self.config.get_path('output_file_path_c4_product', section='Control4Paths')
        if not output_path:
            self.normal_logger.log('Error', f'Cesta k výstupnímu souboru product nebyla nalezena.', 'PRICON004')
            self.messenger.show_error('Error', f'Cesta k výstupnímu souboru product nebyla nalezena.', 'PRICON004', False)
            self.print_window.reset_input_focus()
            return

        try:
            # 💾 Write header and record to file / Zápis hlavičky a záznamu do souboru
            with output_path.open('w') as file:
                file.write(header + '\n')
                file.write(record + '\n')

            # 🗂️ Retrieve trigger directory from config / Získání složky pro spouštěče z konfigurace
            trigger_dir = self.get_trigger_dir()
            if not trigger_dir or not trigger_dir.exists():
                self.normal_logger.log('Error', f'Složka trigger_path neexistuje nebo není zadána.', 'PRICON005')
                self.messenger.show_error('Error', f'Složka trigger_path neexistuje nebo není zadána.', 'PRICON005', False)
                self.print_window.reset_input_focus()
                return

            # ✂️ Create trigger files from values / Vytvoření souborů podle hodnot I=
            for value in trigger_values:
                target_file = trigger_dir / value
                target_file.touch(exist_ok=True)
                # 💬 Inform the user about printing progress / Informace o průběhu tisku
                self.messenger.show_timed_info('Info', f'Prosím čekejte, tisknu etiketu: {value}', 3000)

        except Exception as e:
            # 🛑 Log and display unexpected error / Zaloguj a zobraz neočekávanou chybu
            self.normal_logger.log('Error', f'Chyba zápisu {str(e)}', 'PRICON006')
            self.messenger.show_error('Error', f'{str(e)}', 'PRICON006', False)
            self.print_window.reset_input_focus()

    def product_save_and_print(self, header: str, record: str, trigger_values: list[str]) -> None:
        """
        Extracts header and record for the scanned serial number and writes them to product output file.
        Načte hlavičku a záznam z řádků .lbl pro naskenovaný serial number a zapíše je do výstupního souboru product.

        :param header: extracted header line / extrahovaná hlavička z .lbl
        :param record: extracted record line / extrahovaný záznam z .lbl
        :param trigger_values: list of trigger filenames / seznam názvů souborů spouštěče
        """

        # 📁 Retrieve output file path from config / Získání cesty k výstupnímu souboru z konfigurace
        output_path = self.config.get_path('output_file_path_product', section='ProductPaths')
        if not output_path:
            self.normal_logger.log('Warning', f'Cesta k výstupnímu souboru product nebyla nalezena.', 'PRICON009')
            self.messenger.show_warning('Warning', f'Cesta k výstupnímu souboru product nebyla nalezena.', 'PRICON009')
            self.print_window.reset_input_focus()
            return

        try:
            # 💾 Write header and record to file / Zápis hlavičky a záznamu do souboru
            with output_path.open('w') as file:
                file.write(header + '\n')
                file.write(record + '\n')

            # 🗂️ Retrieve trigger directory from config / Získání složky pro spouštěče z konfigurace
            trigger_dir = self.get_trigger_dir()
            if not trigger_dir or not trigger_dir.exists():
                self.normal_logger.log('Warning', f'Složka trigger_path neexistuje nebo není zadána.', 'PRICON010')
                self.messenger.show_warning('Warning', f'Složka trigger_path neexistuje nebo není zadána.', 'PRICON010')
                self.print_window.reset_input_focus()
                return

            # ✂️ Create trigger files from values / Vytvoření souborů podle hodnot B=
            for value in trigger_values:
                target_file = trigger_dir / value
                target_file.touch(exist_ok=True)
                # 💬 Inform the user about printing progress / Informace o průběhu tisku
                self.messenger.show_timed_info('Info', f'Prosím čekejte, tisknu etiketu: {value}', 3000)

        except Exception as e:
            # 🛑 Log and display unexpected error / Zaloguj a zobraz neočekávanou chybu
            self.normal_logger.log('Error', f'Chyba zápisu {str(e)}', 'PRICON011')
            self.messenger.show_error('Error', f'{str(e)}', 'PRICON011', False)
            self.print_window.reset_input_focus()

    def my2n_save_and_print(self) -> None:
        """
        Extracts My2N token from related report file and writes it into structured output file.
        Načte My2N token ze souboru na základě serial number a uloží jej do výstupního souboru.

        - Cesta k reportu: reports_path / {2054}/{4205}/{42050036.54}
        - Hledá poslední řádek obsahující 'My2N token:'
        - Vytvoří výstupní soubor s hlavičkou a hodnotami
        """
        # 🧠 Loading serial number from input / Načtení serial number z inputu
        serial_number = self.serial_input
        parts = serial_number.split('-')

        # ✂️ Preparing a file name from values / Příprava názvu souboru z hodnot
        base_code = parts[1] + parts[2]
        file_name = f'{base_code}.{parts[0]}'
        subdir1 = f'20{parts[0]}'  # 0036 + 54 = 2054
        subdir2 = parts[1]  # 4205

        # 📁 Getting the path from config / Získání cesty z configu
        reports_path = self.config.get_path('reports_path', section='Paths')
        output_path = self.config.get_path('output_file_path_my2n', section='My2nPaths')

        if not reports_path or not output_path:
            self.normal_logger.log('Error', f'Cesty nejsou definovány v config.ini.', 'PRICON012')
            self.messenger.show_error('Error', f'Cesty nejsou definovány v config.ini.', 'PRICON012', False)
            return

        # 🧩 Final path to the input file / Finální cesta ke vstupnímu souboru
        source_file = reports_path / subdir1 / subdir2 / file_name

        if not source_file.exists():
            self.normal_logger.log('Info', f'Report soubor {source_file} neexistuje.', 'PRICON013')
            self.messenger.show_info('Info', f'Report soubor {source_file} neexistuje.', 'PRICON013')
            return

        try:
            lines = source_file.read_text().splitlines()
        except Exception as e:
            self.normal_logger.log('Error', f'Chyba čtení {str(e)}', 'PRICON014')
            self.messenger.show_error('Error', f'{str(e)}', 'PRICON014', False)
            return

        # 🔎 We find the last occurrence of "My2N token:" / Najdeme poslední výskyt "My2N token:"
        token_line = next((line for line in reversed(lines) if 'My2N token:' in line), None)

        if not token_line:
            self.normal_logger.log('Warning', f'V souboru nebyl nalezen žádný My2N token.', 'PRICON015')
            self.messenger.show_warning('Warning', f'V souboru nebyl nalezen žádný My2N token.', 'PRICON015')
            return

        # ✂️ Token extraction / Extrakce tokenu
        try:
            token = token_line.split('My2N token:')[1].strip()
        except Exception as e:
            self.normal_logger.log('Error', f'Chyba extrakce {str(e)}', 'PRICON016')
            self.messenger.show_error('Error', f'Chyba extrakce {str(e)}', 'PRICON016', False)
            return

        # 📄 Write to output file / Zápis do výstupního souboru
        try:
            with output_path.open('w') as file:
                file.write('"L Vyrobni cislo dlouhe","L Bezpecnostni cislo","P Vyrobni cislo","P Bezpecnostni kod"\n')
                file.write(f'"Serial number:","My2N Security Code:","{serial_number}","{token}"\n')

            self.normal_logger.clear_log('Info', f'{token}')

            # 🗂️ Creating trigger file SF_MY2N_A / Vytvoření trigger souboru SF_MY2N_A
            trigger_dir = self.get_trigger_dir()

            if trigger_dir and trigger_dir.exists():
                try:
                    trigger_file = trigger_dir / 'SF_MY2N_A'
                    trigger_file.touch(exist_ok=True)

                except Exception as e:
                    self.normal_logger.log('Error', f'Chyba trigger souboru {str(e)}', 'PRICON017')
                    self.messenger.show_error('Error', f'Chyba trigger souboru {str(e)}', 'PRICON017', False)
            else:
                self.normal_logger.log('Warning', f'Složka "trigger_path" není definována nebo neexistuje.', 'PRICON018')
                self.messenger.show_warning('Warning', f'Složka "trigger_path" není definována nebo neexistuje.', 'PRICON018')

        except Exception as e:
            self.normal_logger.log('Error', f'Chyba zápisu {str(e)}', 'PRICON019')
            self.messenger.show_error('Error', f'{str(e)}', 'PRICON019', False)

    def get_trigger_groups_for_product(self) -> list[str]:
        """
        Returns all trigger groups (product, control4, my2n) that match product_name from config.
        Vrátí všechny skupiny (product, control4, my2n), které obsahují zadaný produkt z configu.

        :return: List of matching group names / Seznam shodných skupin
        """
        product_name = self.product_name

        matching = []
        for section_key in self.config.config.options('ProductTriggerMapping'):
            raw_list = self.config.config.get('ProductTriggerMapping', section_key)
            items = [i.strip() for i in raw_list.split(',')]
            if product_name in items:
                matching.append(section_key)

        return matching  # e.g. ['product', 'my2n']

    def print_button_click(self):
        """
        Handles print button action by validating input and triggering appropriate save-and-print methods.
        Obsluhuje kliknutí na tlačítko 'Print' validací vstupu a spuštěním příslušných metod podle konfigurace.
        """

        # === 1️⃣ Validate serial number input / Validace vstupu
        if not self.validate_serial_number_input():
            return

        # === 2️⃣ Resolve product trigger groups from config / Načtení skupin produktů podle konfigurace
        triggers = self.get_trigger_groups_for_product()

        # === 3️⃣ Load corresponding .lbl file lines / Načtení řádků ze souboru .lbl
        lbl_lines = self.load_file_lbl()
        if not lbl_lines:
            self.normal_logger.log('Error', f'Soubor .lbl nelze načíst nebo je prázdný!', 'PRICON020')
            self.messenger.show_error('Error', 'Soubor .lbl nelze načíst nebo je prázdný!', 'PRICON020', False)
            return

        # 📌 Execute save-and-print functions as needed / Spuštění odpovídajících funkcí
        if 'product' in triggers and lbl_lines:

            # === 1️⃣ Validate presence of required lines / Validace existence B/D/E řádků
            if not self.validator.validate_input_exists_for_product(lbl_lines, self.serial_input):
                return

            # === 2️⃣ Extract header and record / Získání D= a E= řádků
            result = self.validator.extract_header_and_record(lbl_lines, self.serial_input)
            if not result:
                return

            header, record = result

            # === 3️⃣ Inject prefix to record / Vložení prefixu do správného pole
            new_record = self.validator.validate_and_inject_balice(header, record)
            if new_record is None:
                return

            # === 4️⃣ Inject prefix to record / Vložení prefixu do správného pole
            trigger_values = self.validator.extract_trigger_values(lbl_lines, self.serial_input)
            if not trigger_values:
                return

            # === 5️⃣ Save and print / Spuštění zápisu výstupního souboru
            self.product_save_and_print(header, new_record, trigger_values)

            # === 6️⃣ Log success
            self.normal_logger.clear_log('Info', f'{self.product_name} {self.serial_input}')

        # 📌 Execute control4-save-and-print functions as needed / Spuštění odpovídajících funkcí
        if 'control4' in triggers and lbl_lines:
            # === 1️⃣ Validace vstupních řádků I/J/K
            if not self.validator.validate_input_exists_for_control4(lbl_lines, self.serial_input):
                return

            # === 2️⃣ Získání hlavičky a záznamu z J= a K=
            result = self.validator.extract_header_and_record_c4(lbl_lines, self.serial_input)
            if not result:
                return
            header, record = result

            # === 3️⃣ Získání hodnot z I= řádku
            trigger_values = self.validator.extract_trigger_values_c4(lbl_lines, self.serial_input)
            if not trigger_values:
                return

            # === 4️⃣ Spuštění zápisu pro Control4
            self.control4_save_and_print(header, record, trigger_values)

            # === 5️⃣ Zápis do logu
            self.normal_logger.clear_log('Info', f'Control4 {self.serial_input}')

        # 📌 Execute my2n-save-and-print functions as needed / Spuštění odpovídajících funkcí
        if 'my2n' in triggers:
            self.my2n_save_and_print()

        self.normal_logger.add_blank_line()
        self.print_window.reset_input_focus()

    def handle_exit(self):
        """
        Closes PrintWindow and returns to the previous window.
        Zavře PrintWindow a vrátí se na předchozí okno ve stacku.
        """
        self.print_window.effects.fade_out(self.print_window, duration=1000)
