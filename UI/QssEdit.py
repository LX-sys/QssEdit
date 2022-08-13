# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QssEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QSpinBox
from PyQt5 import QtCore, QtGui, QtWidgets

from GuiLib import QSSEdit
from GuiLib import Tree,Tab
from core.controlShell import ControlShell,ControlGroup


class QssEdit(QMainWindow):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        # 控件组
        self.__control_group = ControlGroup()

        # 控件字典
        self.__control_dict = dict()

        self.setupUi()


        self.myEvent()
    
    def setupUi(self):
        self.setObjectName("self")
        self.resize(1346, 737)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        # -- 左侧树 --
        self.createTree()

        # -- 代码编辑器 --
        self.creatTab()

        self.preview = QStackedWidget(self.splitter_2)
        self.preview.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.preview.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.preview.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.preview.addWidget(self.page_2)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        # ---------------
        # self.ss = ControlShell("QPushButton", "btn", self.page)
        # self.ss.setGeometry(90, 90, 120, 80)
        # self.ss.activate(True)
        # self.__control_group.addControlShell(self.ss)
        # self.__control_group.setActivateControl(*self.ss.name())
        self.addControlShell("QPushButton", "btn", self.page)
        self.addControlShell("QPushButton", "btn2", self.page)
        # ------------

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1346, 23))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)


        self.myStatusbar()

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)

        self.mySplitter()

        QtCore.QMetaObject.connectSlotsByName(self)

    def addControlShell(self,name:str,alias:str,stackedWidget:QStackedWidget,attrs:dict=None):
        ss = ControlShell(name, alias, stackedWidget)
        ss.activate(True)
        self.__control_group.addControlShell(ss)
        self.__control_group.setActivateControl(*ss.name())

    # 创建树
    def createTree(self):
        self.treeWidget = Tree(self.splitter)
        self.treeWidget.setObjectName("treeWidget")

    def creatTab(self):
        self.tabWidget = Tab(self.splitter)
        # self.tabWidget.addTab(QSSEdit(),"default.qss")
        # self.tabWidget.addTab(QSSEdit(),"test.qss")

    # 布局调整
    def mySplitter(self):
        w1 = int(self.width() * 0.65)
        self.splitter_2.setSizes([w1, self.width() - w1])
        self.splitter.setSizes(
            [int(w1 * 0.3), int(w1 * 0.7)]
        )

    # 打开qss文件,进行编辑
    def open_qss(self,file_name:str):
        self.tabWidget.addTab(QSSEdit(),file_name)

    def myEvent(self):
        self.treeWidget.filenameedit.connect(self.open_qss)

    def myStatusbar(self):
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.statusbar.addWidget(QLabel("{}".format(self.__control_group.getActivateControl().name()[1])))

        self.statusbar.addWidget(QLabel("W"))
        self.w = QSpinBox()
        self.statusbar.addWidget(self.w)
        self.h = QSpinBox()
        self.statusbar.addWidget(QLabel("H"))
        self.statusbar.addWidget(self.h)

        self.w.setMinimum(1)
        self.h.setMinimum(1)
        self.w.setMaximum(500)
        self.h.setMaximum(500)

        obj = self.__control_group.getActivateControl().getObj()
        self.w.setValue(obj.width())
        self.h.setValue(obj.height())

        self.w.textChanged.connect(self.w_Event)
        self.h.textChanged.connect(self.h_Event)

    def w_Event(self,w):
        w = int(w)
        obj = self.__control_group.getActivateControl().getObj()
        obj.resize(w,obj.height())
        obj.setMinimumSize(w,obj.height())
        win = self.__control_group.getActivateControl().getSelf()
        win.resize(w+1,win.height())

    def h_Event(self,h):
        h = int(h)
        obj = self.__control_group.getActivateControl().getObj()
        obj.resize(h, obj.height())
        obj.setMinimumSize(h, obj.height())
        win = self.__control_group.getActivateControl().getSelf()
        win.resize(win.width(), h + 1)


    # def textChanged_Event(self):
    #     style = self.code_edit.text()
    #     try:
    #         obj = self.__control_group.getActivateControl().getObj()
    #         obj.setStyleSheet(style)
    #     except Exception as e:
    #         print(e)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "QssEditor"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = QssEdit()
    win.show()

    sys.exit(app.exec_())
    