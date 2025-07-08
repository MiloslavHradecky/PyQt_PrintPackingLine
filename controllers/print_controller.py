# 🖨️ PrintController – handles logic for serial input, validation, and print action
# Řídí logiku vstupu serial number, validaci a spuštění tisku

import re
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
        orders_path = config.get_path('orders_path', section='Paths')

        if not orders_path:
            self.messenger.show_error('Error', 'Konfigurační cesta "orders_path" nebyla nalezena.', 'CTRL401')
            self.reset_input_focus()
            return []

        # 🧩 Sestavení cesty k .lbl souboru
        lbl_file = orders_path / f'{self.print_window.order_code}.lbl'

        if not lbl_file.exists():
            self.messenger.show_info('Warning', f'Soubor {lbl_file} neexistuje.', 'CTRL402')
            self.reset_input_focus()
            return []

        try:
            # 📄 Načtení obsahu souboru
            return lbl_file.read_text().splitlines()
        except Exception as e:
            self.messenger.show_error('Error', str(e), 'CTRL403')
            self.reset_input_focus()
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
            self.reset_input_focus()
            return

        # 📁 Získání cesty z configu
        config = ConfigLoader()
        output_path = config.get_path('output_file_path_c4_product', section='Control4Paths')

        if not output_path:
            self.messenger.show_error('Error', f'Cesta k výstupnímu souboru Control4 nebyla nalezena.', 'CTRL406')
            self.reset_input_focus()
            return

        try:
            # 💾 Zápis hlavičky + záznamu
            with output_path.open('w') as file:
                file.write(header + '\n')
                file.write(record + '\n')

            self.normal_logger.log('Info', f'Control4 záznam uložen.', 'CTRL407')

            # 🗂️ Získání trigger_path z config.ini
            trigger_dir = config.get_path('trigger_path', section='Paths')

            if not trigger_dir or not trigger_dir.exists():
                self.messenger.show_warning('Warning', f'Složka trigger_path neexistuje nebo není zadána.', 'CTRL409')
                self.reset_input_focus()
                return

            # 🔎 Najdeme řádek s I= prefixem
            trigger_line = next((line for line in lbl_lines if line.startswith(key_i)), None)

            if trigger_line:
                try:
                    # ✂️ Rozdělení a vytvoření souborů podle hodnot
                    trigger_values = trigger_line.split('I=')[1].strip().split(';')

                    for value in trigger_values:
                        name = value.strip()
                        if name:
                            target_file = trigger_dir / name  # ⚠️ Bez přípony!
                            target_file.touch(exist_ok=True)

                    self.normal_logger.log('Info', f'Vytvořeno {len(trigger_values)} trigger souborů ve složce "{trigger_dir}".', 'CTRL410')
                    self.reset_input_focus()

                except Exception as e:
                    self.messenger.show_error('Error', f'Chyba při tvorbě souborů z I= {str(e)}', 'CTRL411')
                    self.reset_input_focus()

        except Exception as e:
            self.messenger.show_error('Error', f'Chyba zápisu {str(e)}', 'CTRL408')
            self.reset_input_focus()

    def product_save_and_print(self, lbl_lines: list[str]) -> None:
        """
        Extracts header and record for the scanned serial number and writes them to product output file.
        Načte hlavičku a záznam z řádků .lbl pro naskenovaný serial number a zapíše je do výstupního souboru product.

        - Hledá řádky začínající na: SERIAL+B= a SERIAL+D= a SERIAL+E=
        - Pokud najde hlavičku i záznam, zapíše je do výstupního souboru

        :param lbl_lines: List of lines from .lbl file / Seznam řádků ze souboru
        """
        # 🧠 Získání vstupu ze scanu
        base_input = self.print_window.serial_number_input.text().strip().upper()
        key_b = f'{base_input}B='
        key_d = f'{base_input}D='
        key_e = f'{base_input}E='

        header = None
        record = None

        for line in lbl_lines:
            if line.startswith(key_d):
                header = line.split('D=')[1].strip()
            elif line.startswith(key_e):
                record = line.split('E=')[1].strip()

        # 🚦 Kontrola nálezů
        if not header or not record:
            self.messenger.show_warning('Warning', f'Není dostupná hlavička nebo data pro serial number "{base_input}".', 'CTRL405')
            self.reset_input_focus()
            return

        # 📁 Získání cesty z configu
        config = ConfigLoader()
        output_path = config.get_path('output_file_path_product', section='ProductPaths')

        if not output_path:
            self.messenger.show_error('Error', f'Cesta k výstupnímu souboru product nebyla nalezena.', 'CTRL406')
            self.reset_input_focus()
            return

        try:
            # 💾 Zápis hlavičky + záznamu
            with output_path.open('w') as file:
                file.write(header + '\n')
                file.write(record + '\n')

            self.normal_logger.log('Info', f'Product záznam uložen.', 'CTRL407')

            # 🗂️ Získání trigger_path z config.ini
            trigger_dir = config.get_path('trigger_path', section='Paths')

            if not trigger_dir or not trigger_dir.exists():
                self.messenger.show_warning('Warning', f'Složka trigger_path neexistuje nebo není zadána.', 'CTRL409')
                self.reset_input_focus()
                return

            # 🔎 Najdeme řádek s B= prefixem
            trigger_line = next((line for line in lbl_lines if line.startswith(key_b)), None)

            if trigger_line:
                try:
                    # ✂️ Rozdělení a vytvoření souborů podle hodnot
                    trigger_values = trigger_line.split('B=')[1].strip().split(';')

                    for value in trigger_values:
                        name = value.strip()
                        if name:
                            target_file = trigger_dir / name  # ⚠️ Bez přípony!
                            target_file.touch(exist_ok=True)

                    self.normal_logger.log('Info', f'Vytvořeno {len(trigger_values)} trigger souborů ve složce "{trigger_dir}".', 'CTRL410')
                    self.reset_input_focus()

                except Exception as e:
                    self.messenger.show_error('Error', f'Chyba při tvorbě souborů z B= {str(e)}', 'CTRL411')
                    self.reset_input_focus()

        except Exception as e:
            self.messenger.show_error('Error', f'Chyba zápisu {str(e)}', 'CTRL408')
            self.reset_input_focus()

    def my2n_save_and_print(self) -> None:
        """
        Extracts My2N token from related report file and writes it into structured output file.
        Načte My2N token ze souboru na základě serial number a uloží jej do výstupního souboru.

        - Cesta k reportu: reports_path / {2054}/{4205}/{42050036.54}
        - Hledá poslední řádek obsahující 'My2N token:'
        - Vytvoří výstupní soubor s hlavičkou a hodnotami
        """
        # 🧠 Načtení serial number z inputu
        serial_number = self.print_window.serial_number_input.text().strip().upper()
        parts = serial_number.split('-')

        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            self.messenger.show_warning('Warning', f'Serial number musí být typu 00-0000-0000.', 'MY2N001')
            return

        # ✂️ Příprava názvu souboru z hodnot
        base_code = parts[1] + parts[2]
        file_name = f'{base_code}.{parts[0]}'
        subdir1 = parts[2][:2] + parts[0]  # 0036 + 54 = 2054
        subdir2 = parts[1]  # 4205

        # 📁 Získání cesty z configu
        config = ConfigLoader()
        reports_path = config.get_path('reports_path', section='Paths')
        output_path = config.get_path('output_file_path_my2n', section='My2nPaths')

        if not reports_path or not output_path:
            self.messenger.show_error('Error', f'Cesty nejsou definovány v config.ini.', 'MY2N002')
            return

        # 🧩 Finální cesta ke vstupnímu souboru
        source_file = reports_path / subdir1 / subdir2 / file_name

        if not source_file.exists():
            self.messenger.show_info('Info', f'Report soubor {source_file} neexistuje.', 'MY2N003')
            return

        try:
            lines = source_file.read_text().splitlines()
        except Exception as e:
            self.messenger.show_error('Error', f'Chyba čtení {str(e)}', 'MY2N004')
            return

        # 🔎 Najdeme poslední výskyt "My2N token:"
        token_line = next((line for line in reversed(lines) if 'My2N token:' in line), None)

        if not token_line:
            self.messenger.show_warning('Token nenalezen', 'V souboru nebyl nalezen žádný My2N token.', 'MY2N005')
            return

        # ✂️ Extrakce tokenu
        try:
            token = token_line.split('My2N token:')[1].strip()
        except Exception as e:
            self.messenger.show_error('Error', f'Chyba extrakce {str(e)}', 'MY2N006')
            return

        # 📄 Zápis do výstupního souboru
        try:
            with output_path.open('w') as file:
                file.write('"L Vyrobni cislo dlouhe","L Bezpecnostni cislo","P Vyrobni cislo","P Bezpecnostni kod"\n')
                file.write(f'"Serial number:","My2N Security Code:","{serial_number}","{token}"\n')

            self.normal_logger.log('Info', f'My2N token uložen: {token}', 'MY2N007')

        except Exception as e:
            self.messenger.show_error('Error', f'Chyba zápisu {str(e)}', 'MY2N008')

    def print_button_click(self):
        if not self.validate_serial_number_input():
            return
        self.my2n_save_and_print()
        # lbl_lines = self.load_file_lbl()
        # if lbl_lines:
        #     # self.control4_save_and_print(lbl_lines)
        #     self.product_save_and_print(lbl_lines)

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
