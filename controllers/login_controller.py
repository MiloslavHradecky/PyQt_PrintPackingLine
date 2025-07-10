# 🎛️ LoginController – handles login logic and post-authentication navigation
# Třída LoginController zajišťuje ověření hesla a přechod do další části aplikace

import subprocess
import utils.szv_utils
from core.logger import Logger
from core.messenger import Messenger


class LoginController:
    """
    Main controller for the login process.
    Hlavní řídící třída pro přihlášení uživatele.
    """

    def __init__(self, login_window, window_stack):
        """
        Initializes the LoginController and connects event handlers.
        Inicializuje LoginController a nastaví potřebné reference.

        :param login_window: Reference to LoginWindow / Odkaz na přihlašovací okno
        :param window_stack: WindowStackManager for screen navigation
        """

        # 📌 Store UI references / Uchování referencí na okna
        self.login_window = login_window
        self.window_stack = window_stack

        # 📌 Initialize messenger for user feedback / Zprávy pro uživatele
        self.messenger = Messenger()

        # 🔐 Load decryption engine for login verification / Inicializujeme třídu pro ověření hesla (např. pomocí ID karty)
        self.decrypter = utils.szv_utils.SzvDecrypt()

        self.value_prefix = None
        self.work_order_controller = None

        # 📌 Initialize logging system / Inicializujeme loggery
        self.normal_logger = Logger(spaced=False)
        self.spaced_logger = Logger(spaced=True)

        # 🔗 Connect buttons to handlers / Propojení UI s metodami
        self.login_window.login_button.clicked.connect(self.handle_login)
        self.login_window.exit_button.clicked.connect(self.handle_exit)

    def kill_bartender_processes(self):
        """
        Terminates all running BarTender instances (Cmdr.exe and bartend.exe).
        Ukončí všechny běžící instance BarTender (Cmdr.exe a bartend.exe).
        """
        try:
            subprocess.run('taskkill /f /im cmdr.exe 1>nul 2>nul', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run('taskkill /f /im bartend.exe 1>nul 2>nul', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

        except subprocess.CalledProcessError as e:
            self.normal_logger.log('Error', f'Chyba při ukončování BarTender procesů: {str(e)}', 'LOGCON001')
            self.messenger.show_error('Error', f'{str(e)}', 'LOGCON001', False)

    def handle_login(self):
        """
        Handles login validation and user authentication.
        Zpracuje přihlášení, ověří ID a otevře další okno.

        - Retrieves password from LoginWindow
        - Verifies password via SzvDecrypt
        - Opens WorkOrderWindow if successful
        - Shows warning on failure
        """
        password = self.login_window.password_input.text().strip()  # 🔐 Getting password from input / Získání hesla z inputu
        self.login_window.password_input.clear()

        try:
            if self.decrypter.check_login(password):
                self.value_prefix = utils.szv_utils.get_value_prefix()
                self.kill_bartender_processes()
                self.open_work_order_window()
            else:
                # 🟡 Incorrect password entered
                self.normal_logger.log('Warning', f'Zadané heslo "{password}" není správné!', 'LOGCON002')
                self.messenger.show_warning('Warning', f'Zadané heslo není správné!', 'LOGCON002')
                self.login_window.password_input.clear()
                self.login_window.password_input.setFocus()
        except Exception as e:
            # 🔴 Unexpected login failure
            self.normal_logger.log('Error', f'Neočekávaný problém: {str(e)}', 'LOGCON003')
            self.messenger.show_error('Error', f'{str(e)}', 'LOGCON003', False)
            self.login_window.password_input.clear()
            self.login_window.password_input.setFocus()

    def open_work_order_window(self):
        """
        Opens the WorkOrderWindow upon successful login.
        Otevře další okno aplikace pro zpracování výrobních příkazů.

        - Fades out login window
        - Pushes next window to stack
        """
        from controllers.work_order_controller import WorkOrderController
        self.work_order_controller = WorkOrderController(self.window_stack)
        self.window_stack.push(self.work_order_controller.work_order_window)

    def handle_exit(self):
        """
        Handles application exit from login screen.
        Zpracuje ukončení aplikace z přihlašovacího okna.
        """
        # 💡 This triggers signal destroyed → stack manager does its thing / To spustí signal destroyed → stack manager udělá své
        self.login_window.effects.fade_out(self.login_window, duration=1000)
