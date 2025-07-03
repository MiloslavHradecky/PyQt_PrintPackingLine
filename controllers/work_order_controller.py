from core.logger import Logger
from core.messenger import Messenger
from views.work_order_window import WorkOrderWindow


class WorkOrderController:
    def __init__(self, window_stack):
        self.window_stack = window_stack
        self.work_order_window = WorkOrderWindow(controller=self)

        self.messenger = Messenger()

        # 📌 Inicializace loggerů
        self.normal_logger = Logger(spaced=False)  # ✅ Klasický logger
        self.spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem

        # 📌 Propojení tlačítka s metodou
        self.work_order_window.next_button.clicked.connect(self.on_button_click)
        self.work_order_window.exit_button.clicked.connect(self.handle_exit)

    def on_button_click(self):
        """
        Zpracování události kliknutí na tlačítko:
        - Získá vstupní hodnotu
        - Ověří existenci očekávaných souborů
        - Načte data ze souborů
        - Spustí hlavní aplikační okno nebo zobrazí chybu
        """

        # 📌 1. Zpracování vstupu
        value_input = self.work_order_window.work_order_input.text().strip().upper()
        if not value_input:
            self.messenger.show_warning('Warning', f'Zadejte prosím výrobní příkaz!', 'WORDCON001')
            self.work_order_window.work_order_input.clear()
            self.work_order_window.work_order_input.setFocus()
            return

    def handle_exit(self):
        """Zavře LoginWindow a vrátí se na předchozí okno ve stacku."""
        self.work_order_window.effects.fade_out(self.work_order_window, duration=3000)  # ✅ To spustí signal destroyed → stack manager udělá své
