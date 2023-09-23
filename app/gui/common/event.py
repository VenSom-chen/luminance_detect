from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget


class WinEvent(QWidget):
    """ 总事件处理对象 """
    _events = {}

    # 添加事件处理函数
    def add_event_handler(self, evt: QEvent, handler):
        if self._events.get(evt) is None:
            self._events[evt] = []
        self._events[evt].append(handler)

    # 事件处理中心
    def event(self, evt: QEvent) -> bool:
        handlers = self._events.get(evt.type())
        if handlers is None or len(handlers) == 0:
            return super().event(evt)
        for handler in handlers:
            if handler(evt) is True:
                return True
        return False
