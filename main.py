#!/usr/bin/env python3
__version__ = '2.0.0.0'  # Verze aplikace

from PyQt6.QtWidgets import QApplication
from views.login_window import LoginWindow
from controllers.login_controller import LoginController
from views.splash_screen import SplashScreen
from utils.window_stack import WindowStackManager

window_stack = WindowStackManager()


def main():
    """
    Hlavní vstupní bod aplikace.

    - Inicializuje 'QApplication'
    - Vytváří a zobrazuje 'LoginWindow'
    - Spravuje běh aplikace pomocí 'sys.exit(app.exec())'
    """
    app = QApplication([])

    def launch_login():
        login_window = LoginWindow()  # ❗️vytvoříme okno bez controlleru
        login_controller = LoginController(login_window, window_stack)  # předáme okno controlleru
        login_window.controller = login_controller  # volitelně zpětná reference (pokud používáš)
        window_stack.push(login_window)  # ✅ Tohle je důležité!
        login_window.effects.fade_in(login_window, duration=2000)

    splash = SplashScreen()
    splash.start(launch_login)

    app.exec()


if __name__ == "__main__":
    """
    Hlavní vstupní bod programu.

    - Kontroluje, zda je skript spuštěn přímo (ne jako modul)
    - Volá funkci 'main()'
    """
    main()  # ✅ Spuštění hlavní funkce programu
