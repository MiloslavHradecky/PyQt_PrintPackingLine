#!/usr/bin/env python3
__version__ = '2.0.0.0'  # 🟥 Application version / Verze aplikace

from PyQt6.QtWidgets import QApplication
from views.login_window import LoginWindow
from controllers.login_controller import LoginController
from views.splash_screen import SplashScreen
from utils.window_stack import WindowStackManager

# 📌 Window stack manager for navigation between UI windows / Správce zásobníku oken aplikace
window_stack = WindowStackManager()


def main():
    """
    Main entry point of the application.
    Hlavní vstupní bod aplikace.

    - Initializes QApplication
    - Creates and displays the LoginWindow
    - Starts application event loop via app.exec()
    """
    app = QApplication([])

    def launch_login():
        login_window = LoginWindow()  # ❗️Create the login window without controller / Vytvoříme okno bez controlleru
        login_controller = LoginController(login_window, window_stack)  # 💡 Assign controller to the window / Předáme okno controlleru
        login_window.controller = login_controller
        window_stack.push(login_window)  # 💡 Push the login window onto the stack / Tohle je důležité!
        login_window.effects.fade_in(login_window, duration=2000)

    # 📌 Show splash screen and then launch login window / Zobrazí splash screen a poté spustí přihlašovací okno
    splash = SplashScreen()
    splash.start(launch_login)

    app.exec()


if __name__ == "__main__":
    """
    Checks if script is run directly (not imported).
    Spustí aplikaci pouze při přímém spuštění (ne importem jako modul).
    """
    main()
