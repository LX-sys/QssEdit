# -*- coding:utf-8 -*-
# @time:2022/8/1317:44
# @author:LX
# @file:tab.py
# @software:PyCharm
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt,pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QMainWindow, QWidget, QPushButton, QGridLayout)


class Tab(QTabWidget):
    # 关闭tab发送信号
    removeed = pyqtSignal(str)
    def __init__(self,*args,**kwargs) -> None:
        super(Tab, self).__init__(*args,**kwargs)

        self.__tab = dict()
        # 设置tab可关闭
        self.setTabsClosable(True)

        self.Init()
        self.myEvent()

    # 获取tab
    def getTab(self,name)->QWidget:
        return self.__tab[name][name]

    def addTab(self, widget: QWidget, name: str) -> None:
        self.__tab[name] = {name:widget}
        new_win = QWidget()
        super(Tab, self).addTab(new_win, name)

        gridLayout = QGridLayout(new_win)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)
        gridLayout.addWidget(widget, 0, 0, 1, 1)

    def Init(self):
        pass

    def closeTab_Event(self,index):
        text = self.tabText(index)
        print(text)
        self.removeTab(index)
        self.removeed.emit(text)

    def myEvent(self):
        self.tabCloseRequested.connect(self.closeTab_Event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Tab()
    w.show()
    sys.exit(app.exec_())