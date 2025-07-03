from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon


class Messenger:
    """
    Třída pro správu MessageBox dialogů.

    - Obsahuje metody pro zobrazení informačních, varovných a chybových zpráv
    - Každá zpráva podporuje ID chyby
    - Umožňuje volitelné ukončení aplikace
    """

    def __init__(self, parent=None):
        """Inicializuje objekt Messenger a nastaví výchozí ikony."""
        # 🔍 Základní složka projektu — dvě úrovně nad messenger.py
        base_dir = Path(__file__).parent.parent

        # 📁 Cesta ke složce s ikonami
        icon_dir = base_dir / 'resources' / 'ico'

        # ✅ Ikony pro jednotlivé typy zpráv
        self.error_icon_path = icon_dir / 'error_message.ico'
        self.info_icon_path = icon_dir / 'info_message.ico'
        self.warning_icon_path = icon_dir / 'warning_message.ico'

        self.parent = parent  # ✅ Připojení k hlavnímu oknu
        self.progress_box = None  # ✅ Inicializace progress boxu

    def show_info(self, title, message, error_code=None):
        """
        Zobrazí informační MessageBox.

        :param title: Název okna
        :param message: Textová zpráva
        :param error_code: Volitelné ID chyby (None pro běžné zprávy)
        """
        info_dialog = QMessageBox()
        info_dialog.setIcon(QMessageBox.Icon.Information)
        info_dialog.setWindowIcon(QIcon(str(self.info_icon_path)))  # ✅ Ikona pro info
        info_dialog.setWindowTitle(title)
        info_dialog.setText(f'{message}' if error_code is None else f'[{error_code}]\n{message}')
        info_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        # 📌 Vycentrování okna
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
        Zobrazí varovný MessageBox.

        :param title: Název okna
        :param message: Textová zpráva
        :param error_code: Volitelné ID chyby (None pro běžné varování)
        """
        warning_dialog = QMessageBox()
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowIcon(QIcon(str(self.warning_icon_path)))  # ✅ Ikona pro warning
        warning_dialog.setWindowTitle(title)
        warning_dialog.setText(f'{message}' if error_code is None else f'[{error_code}]\n{message}')
        warning_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # 📌 Vycentrování okna
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
        Zobrazí chybový MessageBox.

        :param title: Název okna
        :param message: Textová zpráva
        :param error_code: Unikátní ID chyby
        :param exit_on_close: Určuje, zda se aplikace po zavření MessageBoxu ukončí
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowIcon(QIcon(str(self.error_icon_path)))  # ✅ Ikona pro error
        error_dialog.setWindowTitle(title)
        error_dialog.setText(f'[{error_code}]\n{message}')
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # 📌 Vycentrování okna
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

        # 📌 Zobrazení a kontrola, zda se má ukončit aplikace
        result = error_dialog.exec()
        if exit_on_close and result == QMessageBox.StandardButton.Ok:
            QApplication.quit()
