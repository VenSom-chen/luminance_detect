from PyQt5.QtWidgets import QMessageBox, QWidget


class MessageBox:
    def __init__(self, widget: QWidget):
        self._widget = widget

    def ask(self, title, text, buttons=QMessageBox.Yes | QMessageBox.No, default_btn=QMessageBox.NoButton):
        mbox = self._setting_mbox(QMessageBox.Question, title, text, buttons, default_btn)
        mbox.button(QMessageBox.Yes).setText("是")
        mbox.button(QMessageBox.No).setText("否")
        return mbox.exec_()

    def info(self, title, text, buttons=QMessageBox.Ok, default_btn=QMessageBox.NoButton):
        mbox = self._setting_mbox(QMessageBox.Information, title, text, buttons, default_btn)
        mbox.button(QMessageBox.Ok).setText("确认")
        return mbox.exec_()

    def warn(self, title, text, buttons=QMessageBox.Ok, default_btn=QMessageBox.NoButton):
        mbox = self._setting_mbox(QMessageBox.Warning, title, text, buttons, default_btn)
        mbox.button(QMessageBox.Ok).setText("返回")
        return mbox.exec_()

    def error(self, title, text, buttons=QMessageBox.Ok, default_btn=QMessageBox.NoButton):
        mbox = self._setting_mbox(QMessageBox.Critical, title, text, buttons, default_btn)
        mbox.button(QMessageBox.Ok).setText("返回")
        return mbox.exec_()

    def _setting_mbox(self, icon, title, text, buttons=QMessageBox.Yes | QMessageBox.No,
                      default_btn=QMessageBox.NoButton):
        mbox = QMessageBox(self._widget)
        mbox.setWindowTitle(title)
        mbox.setText(text)
        mbox.setStandardButtons(buttons)
        mbox.setDefaultButton(default_btn)
        mbox.setIcon(icon)
        return mbox
