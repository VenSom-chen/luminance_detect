from app.controller.main_win_ctr import MainWinController
from app.gui.main_win import main_window

class App:
    def __init__(self):
        self.mw = main_window()
        self.ctr = []
        self.init_controller()

    def start(self):
        self.mw.show()

    def init_controller(self):
        self.ctr.append(MainWinController())