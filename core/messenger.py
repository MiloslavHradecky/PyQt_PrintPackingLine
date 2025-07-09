# 📬 Messenger – user-facing message dialogs with icons and optional app exit
# Správce zpráv aplikace (info, warning, error) s podporou zarovnání a ikon

from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer


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
        self._show_dialog(
            title=title,
            message=message,
            error_code=error_code,
            icon=QMessageBox.Icon.Information,
            icon_path=self.info_icon_path
        )

    def show_warning(self, title, message, error_code=None):
        """
        Shows a warning dialog.
        Zobrazí varování uživateli.

        :param title: Window title
        :param message: Text to display
        :param error_code: Optional error tag
        """
        self._show_dialog(
            title=title,
            message=message,
            error_code=error_code,
            icon=QMessageBox.Icon.Warning,
            icon_path=self.warning_icon_path
        )

    def show_error(self, title, message, error_code, exit_on_close: bool = False):
        """
        Shows an error message and optionally quits app.
        Zobrazí chybu a volitelně ukončí aplikaci.

        :param title: Window title
        :param message: Message to show
        :param error_code: Required ID code
        :param exit_on_close: Whether app should quit after closing
        """
        result = self._show_dialog(
            title=title,
            message=message,
            error_code=error_code,
            icon=QMessageBox.Icon.Critical,
            icon_path=self.error_icon_path
        )

        if exit_on_close and result == QMessageBox.StandardButton.Ok:
            QApplication.quit()

    def show_timed_info(self, title: str, message: str, duration_ms: int = 3000):
        """
        Shows a transient informational dialog that closes automatically after duration.
        Zobrazí informační okno, které se automaticky zavře po zadané době.

        :param title: Window title / Název okna
        :param message: Message to display / Zobrazená zpráva
        :param duration_ms: How long to show (in milliseconds) / Doba zobrazení v milisekundách
        """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setWindowIcon(QIcon(str(self.info_icon_path)))
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)  # ⛔ No button / Žádné tlačítko

        dialog.adjustSize()

        # 📍 Placement in the centre / Umístění do středu
        if self.parent:
            center = self.parent.geometry().center()
        else:
            center = QApplication.primaryScreen().availableGeometry().center()

        dialog_rect = dialog.geometry()
        dialog.move(center.x() - dialog_rect.width() // 2,
                    center.y() - dialog_rect.height() // 2)

        dialog.show()

        # ⏲️ Setting the automatic closing / Nastavení automatiky na zavření
        QTimer.singleShot(duration_ms, dialog.accept)

    def _show_dialog(self, title, message, error_code, icon, icon_path):
        """
        Internal shared dialog rendering method.
        Interní metoda pro vykreslení libovolného dialogu.

        :return: Clicked button (used for exit handling)
        """
        dialog = QMessageBox()
        dialog.setIcon(icon)
        dialog.setWindowIcon(QIcon(str(icon_path)))
        dialog.setWindowTitle(title)
        dialog.setText(f'{message}' if error_code is None else f'[{error_code}]\n{message}')
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        dialog.adjustSize()

        if self.parent:
            parent_center = self.parent.geometry().center()
            dialog_rect = dialog.geometry()
            dialog.move(parent_center.x() - dialog_rect.width() // 2,
                        parent_center.y() - dialog_rect.height() // 2)
        else:
            screen = QApplication.primaryScreen()
            screen_center = screen.availableGeometry().center()
            dialog_rect = dialog.geometry()
            dialog.move(screen_center.x() - dialog_rect.width() // 2,
                        screen_center.y() - dialog_rect.height() // 2)

        return dialog.exec()
