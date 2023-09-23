import threading

from PyQt5.QtWidgets import QMainWindow

from app.gui.common.event import WinEvent
from app.gui.ui.win import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow,WinEvent):
    _instance_lock = threading.Lock()
    _instance = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @classmethod
    def instance(cls):
        if cls._instance is not None:
            return cls._instance
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance


def main_window():
    return MainWindow.instance()
