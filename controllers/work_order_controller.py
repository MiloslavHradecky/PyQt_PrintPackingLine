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
