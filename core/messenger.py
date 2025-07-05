# 📬 Messenger – user-facing message dialogs with icons and optional app exit
# Správce zpráv aplikace (info, warning, error) s podporou zarovnání a ikon

from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon


class Messenger:
    """
    Shows styled pop-up dialogs to communicate with users.
    Zobrazování zpráv (informace, varování, chyby) pomocí QMessageBox.
    """

    def __init__(self, parent=None):
        """
        Initializes icon paths and optional parent for centering.
        Inicializace cest k ikonám a rodičovského okna (pro zarovnání).

        :param parent: Optional reference to a parent QWidget
        """
        # 🔍 Project base - two levels above messenger.py / Základní složka projektu — dvě úrovně nad messenger.py
        base_dir = Path(__file__).parent.parent

        # 📁 Path to the folder with icons / Cesta ke složce s ikonami
        icon_dir = base_dir / 'resources' / 'ico'

        # 📌 Icons for each message type / Ikony pro jednotlivé typy zpráv
        self.error_icon_path = icon_dir / 'error_message.ico'
        self.info_icon_path = icon_dir / 'info_message.ico'
        self.warning_icon_path = icon_dir / 'warning_message.ico'

        self.parent = parent  # ✅ Connecting to the main window / Připojení k hlavnímu oknu

    def show_info(self, title, message, error_code=None):
        """
        Shows an informational dialog.
        Zobrazí informační dialog.

        :param title: Window title / Název okna
        :param message: Displayed text / Zpráva
        :param error_code: Optional error ID
        """
        info_dialog = QMessageBox()
        info_dialog.setIcon(QMessageBox.Icon.Information)
        info_dialog.setWindowIcon(QIcon(str(self.info_icon_path)))
        info_dialog.setWindowTitle(title)
        info_dialog.setText(f'{message}' if error_code is None else f'[{error_code}]\n{message}')
        info_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # 📌 Centering the window / Vycentrování okna
        info_dialog.adjustSize()
        if self.parent:
            parent_center = self.parent.geometry().center()
            dialog_rect = info_dialog.geometry()
            info_dialog.move(parent_center.x() - dialog_rect.width() // 2,
                             parent_center.y() - dialog_rect.height() // 2)
        else:
            screen = QApplication.primaryScreen()
            screen_rect = screen.availableGeometry()
            screen_center = screen_rect.center()
            dialog_rect = info_dialog.geometry()
            info_dialog.move(screen_center.x() - dialog_rect.width() // 2,
                             screen_center.y() - dialog_rect.height() // 2)
        info_dialog.exec()

    def show_warning(self, title, message, error_code=None):
        """
        Shows a warning dialog.
        Zobrazí varování uživateli.

        :param title: Window title
        :param message: Text to display
        :param error_code: Optional error tag
        """
        warning_dialog = QMessageBox()
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowIcon(QIcon(str(self.warning_icon_path)))
        warning_dialog.setWindowTitle(title)
        warning_dialog.setText(f'{message}' if error_code is None else f'[{error_code}]\n{message}')
        warning_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # 📌 Centering the window / Vycentrování okna
        warning_dialog.adjustSize()
        if self.parent:
            parent_center = self.parent.geometry().center()
            dialog_rect = warning_dialog.geometry()
            warning_dialog.move(parent_center.x() - dialog_rect.width() // 2,
                                parent_center.y() - dialog_rect.height() // 2)
        else:
            screen = QApplication.primaryScreen()
            screen_rect = screen.availableGeometry()
            screen_center = screen_rect.center()
            dialog_rect = warning_dialog.geometry()
            warning_dialog.move(screen_center.x() - dialog_rect.width() // 2,
                                screen_center.y() - dialog_rect.height() // 2)
        warning_dialog.exec()

    def show_error(self, title, message, error_code, exit_on_close: bool = False):
        """
        Shows an error message and optionally quits app.
        Zobrazí chybu a volitelně ukončí aplikaci.

        :param title: Window title
        :param message: Message to show
        :param error_code: Required ID code
        :param exit_on_close: Whether app should quit after closing
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowIcon(QIcon(str(self.error_icon_path)))
        error_dialog.setWindowTitle(title)
        error_dialog.setText(f'[{error_code}]\n{message}')
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # 📌 Centering the window / Vycentrování okna
        error_dialog.adjustSize()
        if self.parent:
            parent_center = self.parent.geometry().center()
            dialog_rect = error_dialog.geometry()
            error_dialog.move(parent_center.x() - dialog_rect.width() // 2,
                              parent_center.y() - dialog_rect.height() // 2)
        else:
            screen = QApplication.primaryScreen()
            screen_rect = screen.availableGeometry()
            screen_center = screen_rect.center()
            dialog_rect = error_dialog.geometry()
            error_dialog.move(screen_center.x() - dialog_rect.width() // 2,
                              screen_center.y() - dialog_rect.height() // 2)

        # 📌 To view and check whether to quit an application / Zobrazení a kontrola, zda se má ukončit aplikace
        result = error_dialog.exec()
        if exit_on_close and result == QMessageBox.StandardButton.Ok:
            QApplication.quit()
