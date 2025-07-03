import utils.szv_utils
from core.logger import Logger
from core.messenger import Messenger


class LoginController:
    """
    Hlavní řídící třída aplikace.
    """

    def __init__(self, login_window, window_stack):
        """
        Inicializuje 'LoginController' a nastaví jeho hlavní atributy.
        :param login_window: Reference na přihlašovací okno ('LoginWindow')
        """

        # 📌 Uložení referencí na okna aplikace
        self.login_window = login_window  # ✅ Uchováme referenci na 'LoginWindow'
        self.window_stack = window_stack  # ✅ uchováme stack
        self.messenger = Messenger()  # ✅ Inicializujeme instanci 'Messenger' pro správu zpráv

        # 📌 Inicializace třídy 'SzvDecrypt' pro dešifrování přihlášení
        self.decrypter = utils.szv_utils.SzvDecrypt()  # ✅ Načteme dešifrovací třídu
        self.value_prefix = None

        self.work_order_controller = None

        # 📌 Inicializace loggerů
        self.normal_logger = Logger(spaced=False)  # ✅ Klasický logger
        self.spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem

        # 📌 Propojení tlačítka s metodou
        self.login_window.login_button.clicked.connect(self.handle_login)
        self.login_window.exit_button.clicked.connect(self.handle_exit)

    def handle_login(self):
        """
        Ověří přihlašovací heslo a provede autentizaci uživatele.
        - Získá zadané heslo z 'LoginWindow'
        - Ověří správnost hesla pomocí 'SzvDecrypt'
        - Při úspěšném přihlášení otevře 'WorkOrderWindow'
        - Při chybě zobrazí varování uživateli
        """
        password = self.login_window.input_password.text().strip()  # ✅ Získání hesla z inputu
        self.login_window.input_password.clear()

        try:
            if self.decrypter.check_login(password):
                self.value_prefix = utils.szv_utils.get_value_prefix()  # ✅ Načtení hodnoty z model.py
                self.open_work_order_window()  # ✅ Po úspěšném přihlášení otevřeme WorkOrderWindow
            else:
                self.normal_logger.log('Warning', f'Zadané heslo "{password}" není správné!', 'LOGCON001')
                self.messenger.show_warning('Warning', f'Zadané heslo není správné!', 'LOGCON001')
                self.login_window.input_password.clear()
                self.login_window.input_password.setFocus()
        except Exception as e:
            self.normal_logger.log('Error', f'Neočekávaný problém: {str(e)}', 'LOGCON002')
            self.messenger.show_error('Error', f'{str(e)}', 'LOGCON002', False)
            self.login_window.input_password.clear()
            self.login_window.input_password.setFocus()

    def open_work_order_window(self):
        """
        Otevře 'WorkOrderWindow' pro výběr produktu.

        - Po úspěšném přihlášení se 'LoginWindow' zavře
        - 'WorkOrderWindow' uchovává referenci na 'ControllerApp'
        """
        from controllers.work_order_controller import WorkOrderController
        self.work_order_controller = WorkOrderController(self.window_stack)
        self.window_stack.push(self.work_order_controller.work_order_window)

    def handle_exit(self):
        """Zavře LoginWindow a vrátí se na předchozí okno ve stacku."""
        self.login_window.effects.fade_out(self.login_window, duration=3000)  # ✅ To spustí signal destroyed → stack manager udělá své
