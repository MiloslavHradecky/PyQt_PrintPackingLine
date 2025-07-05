# 🪟 WindowStackManager – simple navigation stack for multi-window flow
# 🪟 Správce zásobníku oken pro přepínání mezi jednotlivými obrazovkami

class WindowStackManager:
    def __init__(self):
        """
        Initializes the window stack list.
        Inicializuje prázdný zásobník oken.
        """
        self._stack = []

    def push(self, window):
        """
        Pushes a new window onto the stack.
        Přidá nové okno na vrchol zásobníku.

        - Hides the current window (if any)
        - Connects a callback to close the window
        - Displays a new window
        """
        if self._stack:
            self._stack[-1].hide()
        self._stack.append(window)
        window.destroyed.connect(self._on_window_closed)
        window.show()

    def pop(self):
        """
        Pops the top window and shows the previous one (if any).
        Odebere aktuální okno a zobrazí předchozí (pokud existuje).
        """
        if not self._stack:
            return None

        closing = self._stack.pop()

        if self._stack:
            previous = self._stack[-1]
            if not previous.isVisible():
                previous.show()

        return closing

    def _on_window_closed(self):
        """
        Triggered automatically when any window is closed.
        Automaticky vyvoláno při zavření jakéhokoliv okna.
        """
        self.pop()
