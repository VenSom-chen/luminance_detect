from PyQt5.QtCore import QObject

from app.controller.common.mbox import MessageBox
from app.gui.main_win import main_window



class BaseCtr(QObject):
    def __init__(self):
        super().__init__()
        self.mw = main_window()
        self.mbox = MessageBox(self.mw)