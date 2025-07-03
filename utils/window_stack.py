class WindowStackManager:
    def __init__(self):
        self._stack = []

    def push(self, window):
        if self._stack:
            self._stack[-1].hide()
        self._stack.append(window)
        window.destroyed.connect(self._on_window_closed)
        window.show()

    def pop(self):
        if not self._stack:
            return None

        closing = self._stack.pop()

        if self._stack:
            previous = self._stack[-1]
            if not previous.isVisible():
                previous.show()

        return closing

    def _on_window_closed(self):
        self.pop()
