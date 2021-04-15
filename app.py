import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from ui.design import *


class DlgMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())