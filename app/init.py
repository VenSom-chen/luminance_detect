from gui.main_win import main_window

class App:
    def __init__(self):
        self.mw = main_window()

    def start(self):
        self.mw.show()
