import os

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMessageBox, qApp

from app.controller.base import BaseCtr


class WinActivateCtr(BaseCtr):
    def __init__(self):
        super().__init__()
        self.front_box_updated = False

        # 函数初始化
        self.init_qss()
        self.init_event()

    def init_qss(self):
        with open('app/gui/qss/i.qss', 'r', encoding='utf-8') as file:
            qApp.setStyleSheet(file.read())

    def init_event(self):
        self.mw.add_event_handler(QEvent.Close, self.on_close_event)
        self.mw.add_event_handler(QEvent.Resize, self.on_resize_event)
        self.mw.add_event_handler(QEvent.Show, self.on_show_event)

    def on_close_event(self, event):
        reply = self.mbox.ask('提示', "确认退出吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    def on_resize_event(self, event):
        # print("窗口大小发生变化")
        pass

    def on_show_event(self, event):
        print("窗口显示事件")
        if not self.front_box_updated:
            self.front_box_updated = True
