from pathlib import Path
from core.logger import Logger
from core.messenger import Messenger
from views.print_window import PrintWindow


class PrintController:
    def __init__(self, window_stack):
        self.window_stack = window_stack
        self.print_window = PrintWindow(controller=self)

        self.messenger = Messenger()
        self.orders_dir = None
        self.lbl_file = None
        self.nor_file = None
        self.lines = None
        self.found_product_name = None

        # 📌 Inicializace loggerů
        self.normal_logger = Logger(spaced=False)  # ✅ Klasický logger
        self.spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem

        # 📌 Propojení tlačítka s metodou
        self.print_window.print_button.clicked.connect(self.print_button_click)
        self.print_window.exit_button.clicked.connect(self.handle_exit)

    def print_button_click(self):
        pass

    def handle_exit(self):
        """Zavře PrintWindow a vrátí se na předchozí okno ve stacku."""
        self.print_window.effects.fade_out(self.print_window, duration=2000)  # ✅ To spustí signal destroyed → stack manager udělá své
