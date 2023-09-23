from app.controller.common.mbox import MessageBox
from app.controller import main_win_ctr,activate
from app.gui.main_win import main_window

class App:
    def __init__(self):
        self.mw = main_window()
        self.mbox = MessageBox(self.mw)
        self.ctr = []
        self.init_controller()

    def start(self):
        self.mw.show()

    def init_controller(self):
        self.ctr.append(main_win_ctr.MainWinController())
        self.ctr.append(activate.WinActivateCtr())