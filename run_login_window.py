# run_login_window.py

from PyQt6.QtWidgets import QApplication
from views.login_window import LoginWindow

app = QApplication([])

window = LoginWindow()
window.show()  # Zobrazíme bez animací
app.exec()
