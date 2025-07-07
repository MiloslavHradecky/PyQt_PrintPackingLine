# 🧭 WorkOrderController – Manages scanning logic and transitions to printing
# Řídící třída pro zadání pracovního příkazu a přechod na tisk

from pathlib import Path
from core.logger import Logger
from core.messenger import Messenger
from views.work_order_window import WorkOrderWindow


class WorkOrderController:
    def __init__(self, window_stack):
        """
        Initializes controller logic, event binding and file setup.
        Inicializace controlleru, napojení tlačítek a výchozí stavy.
        """
        self.window_stack = window_stack
        self.work_order_window = WorkOrderWindow(controller=self)

        # 🔔 User feedback system / Systém hlášení zpráv
        self.messenger = Messenger()

        # 📂 Paths and file references / Cesty a soubory
        self.orders_dir = None
        self.lbl_file = None
        self.nor_file = None

        # 📄 Parsed data / Načtené hodnoty
        self.lines = None
        self.found_product_name = None

        self.print_controller = None
        self.print_window = None

        # 📌 Logging setup / Nastavení loggeru
        self.normal_logger = Logger(spaced=False)
        self.spaced_logger = Logger(spaced=True)

        # 📌 Button actions / Napojení tlačítek
        self.work_order_window.next_button.clicked.connect(self.work_order_button_click)
        self.work_order_window.exit_button.clicked.connect(self.handle_exit)

    def work_order_button_click(self):
        """
        Triggered on 'Continue' click.
        Spuštěno po stisknutí tlačítka 'Pokračuj'.

        - Validates input
        - Checks .lbl and .nor file existence
        - Parses .nor file and validates order
        - Loads label content and launches print controller
        """

        # 📌 Processing of input / Zpracování vstupu
        value_input = self.work_order_window.work_order_input.text().strip().upper()
        if not value_input:
            self.messenger.show_warning('Warning', f'Zadejte prosím výrobní příkaz!', 'WORDCON001')
            self.reset_input_focus()
            return

        # 📁 Construct paths / Sestavení cest
        self.orders_dir = Path('T:/Prikazy')
        self.lbl_file = self.orders_dir / f'{value_input}.lbl'
        self.nor_file = self.orders_dir / f'{value_input}.nor'

        # ❌ If file not found / Příkaz neexistuje
        if not self.lbl_file.exists() or not self.nor_file.exists():
            self.lines = []
            self.found_product_name = None
            self.normal_logger.log('Warning', f'Soubor {self.lbl_file} nebo {self.nor_file} nebyl nalezen!', 'WORDCON002')
            self.messenger.show_warning('Warning', f'Soubor {self.lbl_file} nebo {self.nor_file} nebyl nalezen!', 'WORDCON002')
            self.reset_input_focus()
            return

        try:
            with self.nor_file.open('r') as file:
                first_line = file.readline().strip()
                parts = first_line.split(';')

                if len(parts) >= 2:
                    nor_order_code = parts[0].lstrip('$').upper()
                    product_name = parts[1].strip()

                    if nor_order_code != value_input:
                        self.normal_logger.log('Warning', f'Výrobní příkaz v souboru .NOR ({nor_order_code}) neodpovídá zadanému vstupu ({value_input})!', 'WORDCON003')
                        self.messenger.show_warning('Warning', f'Výrobní příkaz v souboru .NOR ({nor_order_code}) neodpovídá zadanému vstupu ({value_input})!', 'WORDCON003')
                        self.reset_input_focus()
                        return

                    self.found_product_name = product_name
                    self.lines = self.load_file(self.lbl_file)

                    # 📌 Tady zavoláme další okno:
                    self.open_app_window(order_code=value_input, product_name=product_name)
                    self.reset_input_focus()

                else:
                    self.normal_logger.log('Warning', f'Řádek v souboru {self.nor_file} nemá očekávaný formát.', 'WORDCON004')
                    self.messenger.show_warning('Warning', f'Řádek v souboru {self.nor_file} nemá očekávaný formát.', 'WORDCON004')
                    self.reset_input_focus()
                    return
        except Exception as e:
            self.normal_logger.log('Error', f'Neočekávaná chyba při zpracování .NOR souboru: {e}', 'WORDCON005')
            self.messenger.show_error('Error', f'{e}', 'WORDCON005', exit_on_close=False)
            self.reset_input_focus()
            return

    def load_file(self, file_path: Path) -> list[str]:
        """
        Loads text content from file.
        Načte obsah souboru a vrátí jako list řádků.
        """
        try:
            return file_path.read_text().splitlines()
        except Exception as e:
            self.normal_logger.log('Error', f'Soubor {file_path} se nepodařilo načíst: {e}', 'WORDCON006')
            self.messenger.show_error('Error', f'{e}', 'WORDCON006', False)
            return []

    def open_app_window(self, order_code, product_name):
        """
        Instantiates PrintController and launches next window.
        Vytvoří PrintController a otevře další okno (tisk).
        """
        from controllers.print_controller import PrintController
        self.print_controller = PrintController(self.window_stack, order_code, product_name)
        self.window_stack.push(self.print_controller.print_window)

    def reset_input_focus(self):
        """
        Clears the input field and sets focus back to it.
        Vymaže vstupní pole a nastaví znovu focus.
        """
        self.work_order_window.work_order_input.clear()
        self.work_order_window.work_order_input.setFocus()

    def handle_exit(self):
        """
        Closes the current window with fade-out effect.
        Zavře aktuální okno a vrátí se zpět ve stacku.
        """
        self.work_order_window.effects.fade_out(self.work_order_window, duration=2000)
