'''

    通用Widget抽象类
'''

from PyQt5.QtWidgets import QWidget, QMainWindow,QFrame

class GenericWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(GenericWidget, self).__init__(*args, **kwargs)

        self.setUI()

    def setUI(self):
        pass

    def myEvent(self):
        pass


class GenericMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GenericMainWindow, self).__init__(*args, **kwargs)

        self.setUI()

    def setUI(self):
        pass

    def myEvent(self):
        pass


class GenericFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(GenericFrame, self).__init__(*args, **kwargs)

        self.setUI()

    def setUI(self):
        pass

    def myEvent(self):
        pass