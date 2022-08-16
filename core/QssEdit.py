# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QssEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import QtCore, QtWidgets

from GuiLib import QSSEdit
from GuiLib import Tree,Tab,MenuSys
from core.controlShell import ControlShell,ControlGroup

from core.newControl import NewControl


class QssEdit(QMainWindow):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        # 控件组
        self.__control_group = ControlGroup()

        # 控件工厂
        self.newc = NewControl()

        # 控件字典   树:(控件名称,别名)
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
        self.preview.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.preview.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.preview.addWidget(self.page_2)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1346, 23))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        # 状态栏
        self.myStatusbar()
        # 菜单
        self.myMenu()

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)

        # 布局调整
        self.mySplitter()

        # QtCore.QMetaObject.connectSlotsByName(self)


    def addControlShell(self,name=None,alias:str=None,parent=None,attrs:dict=None):
        ss = ControlShell(name, alias, parent)
        if ss.is_successful():
            ss.show()   # 这句必须写,不然无法显示
            ss.activate(True)
            self.__control_group.addControlShell(ss)
            self.__control_group.setActivateControl(*ss.name())
            return True

    # 创建树
    def createTree(self):
        self.treeWidget = Tree(self.splitter)
        self.treeWidget.setObjectName("treeWidget")
        # self.treeWidget.createTree({"defuat":[]})


    def creatTab(self):
        self.tabWidget = Tab(self.splitter)

    # 布局调整
    def mySplitter(self):
        w1 = int(self.width() * 0.65)
        self.splitter_2.setSizes([w1, self.width() - w1])
        self.splitter.setSizes(
            [int(w1 * 0.3), int(w1 * 0.7)]
        )

    # 文本改变事件
    def textChanged_Event(self,qss:QSSEdit):
        '''

        :param tab_name:  tab名称
        :param qss:
        :return:
        '''
        try:
            self.__control_group.getActivateControl().setStyleSheet(qss.text())
        except:
            pass

    # 打开qss文件,进行编辑
    def open_qss(self,file_name:str):
        if self.tabWidget.is_tab(file_name):
            self.tabWidget.focusTab(file_name)
        else:
            print("open qss")
            qss_edit = QSSEdit()  # 每个tab只创建一次
            qss_edit.textChanged.connect(lambda: self.textChanged_Event(qss_edit))
            self.tabWidget.addTab(qss_edit,file_name)
            self.tabWidget.focusTab(file_name)

        name = self.__control_dict[file_name][0]
        alias = self.__control_dict[file_name][1]
        # 切换控件
        self.__control_group.setActivateControl(name,alias)
        # print("控件切换成功")

    def new_control_Event(self,info:dict):
        name = info["name"]
        control = info["control"]
        if self.addControlShell(control, name,self.page):
            self.treeWidget.createTree({"defuat":[name+".qss"]})
            self.__control_dict[name+".qss"]=(control,name)

    #  切换tab
    def change_tab_Event(self,index):
        file_name = self.tabWidget.tabText(index)
        name = self.__control_dict[file_name][0]
        alias = self.__control_dict[file_name][1]
        # 切换控件
        self.__control_group.setActivateControl(name, alias)

    def myEvent(self):
        self.treeWidget.filenameedit.connect(self.open_qss)
        self.tabWidget.tabBarClicked.connect(self.change_tab_Event)
        # 新建
        self.newc.successfuled.connect(self.new_control_Event)

    def myMenu(self):
        self.menu = MenuSys(self)
        self.menu.addMenuHeader(["控件", "关于"])
        self.menu.addMenuChild("控件", ["新建控件"])
        self.menu.addMenuChild("关于", ["Qss编辑器"])
        self.menu.connect("控件", "新建控件", self.newControl)

    def newControl(self):
        self.newc.show()


    # 状态栏
    def myStatusbar(self):
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # self.statusbar.addWidget(QLabel("{}".format(self.__control_group.getActivateControl().name()[1])))
        #
        # self.statusbar.addWidget(QLabel("W"))
        # self.w = QSpinBox()
        # self.statusbar.addWidget(self.w)
        # self.h = QSpinBox()
        # self.statusbar.addWidget(QLabel("H"))
        # self.statusbar.addWidget(self.h)
        #
        # self.w.setMinimum(1)
        # self.h.setMinimum(1)
        # self.w.setMaximum(500)
        # self.h.setMaximum(500)
        #
        # obj = self.__control_group.getActivateControl().getObj()
        # self.w.setValue(obj.width())
        # self.h.setValue(obj.height())
        #
        # self.w.textChanged.connect(self.w_Event)
        # self.h.textChanged.connect(self.h_Event)

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


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "QssEditor"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = QssEdit()
    win.show()

    sys.exit(app.exec_())
    