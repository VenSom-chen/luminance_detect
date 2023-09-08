import sys

from PyQt5.QtWidgets import QApplication

from app import init

app = QApplication(sys.argv)
App = init.App()
App.start()
sys.exit(app.exec_())

