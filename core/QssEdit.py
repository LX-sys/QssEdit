import sys
import webbrowser

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import QtCore, QtWidgets

from GuiLib import QSSEdit,TreeEdit
from GuiLib import Tree,Tab,MenuSys
from core.controlShell import ControlShell,ControlGroup

from core.newControl import NewControl

# 在不同的目录下,键相同的名称xx.qss会导致打开tab时出现问题

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
        self.tree_edit = TreeEdit(self.splitter_2)
        self.tree_edit.setCloseMouseRight(False)

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


        # 布局调整
        self.mySplitter()

        # QtCore.QMetaObject.connectSlotsByName(self)

    def getControlInfo(self,file_name:str)->tuple:
        name = self.__control_dict[file_name]["type"]
        alias = self.__control_dict[file_name]["alias"]
        return name,alias

    def addControlInfo(self,name:str,control:str):
        self.__control_dict[name]={"type":control,"alias":name}

    def addControlShell(self,name=None,alias:str=None,parent=None,attrs:dict=None):
        ss = ControlShell(name, alias, parent)
        if ss.is_successful():
            ss.show()   # 这句必须写,不然无法显示
            ss.activate(True)
            self.__control_group.addControlShell(ss)
            self.__control_group.setActivateControl(*ss.name())
            return True

    # 布局调整
    def mySplitter(self):
        w1 = int(self.width() * 0.65)
        self.splitter_2.setSizes([w1, self.width() - w1])

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
    def open_qss(self,file_name:str,qss_edit:QSSEdit):
        # 每个tab只创建一次事件
        qss_edit.textChanged.connect(lambda: self.textChanged_Event(qss_edit))
        self.tree_edit.focusTab(file_name)
        # 切换控件
        self.__control_group.setActivateControl(*self.getControlInfo(file_name))
        # print("控件切换成功")

    # 新建控件-菜单事件
    def new_control_Event(self,info:dict):
        name = info["name"]
        control = info["control"]
        if self.tree_edit.createTreeFile(name):
            qss_edit = QSSEdit()
            self.tree_edit.addTab(qss_edit,name)

            name = self.tree_edit.fullPath(name)

            self.addControlShell(control, name, self.page)
            self.addControlInfo(name,control)
            self.open_qss(name,qss_edit)

    #
    def rightClicked_Event(self):
        self.newc.show()

    # 切换tab,激活控件
    def change_tab_Event(self,index):
        file_name = self.tree_edit.getCurrentTab(index)
        # 切换控件(激活控件)
        self.__control_group.setActivateControl(*self.getControlInfo(file_name))


    def myEvent(self):
        self.tree_edit.treeRightClicked.connect(lambda :self.rightClicked_Event())
        # 点击树节点时切换tab,并激活控件
        self.tree_edit.treeLeftClicked.connect(lambda full_path:
                                               self.__control_group.setActivateControl(*self.getControlInfo(full_path)))
        self.tree_edit.switchTab.connect(self.change_tab_Event)
        # 新建
        self.newc.successfuled.connect(self.new_control_Event)

    # Qt样式官网
    def qss_official_Event(self):
        # 跳转到浏览器
        webbrowser.open("https://doc.qt.io/qt-5/stylesheet-reference.html")

    def myMenu(self):
        self.menu = MenuSys(self)
        self.menu.addMenuHeader(["控件", "文档", "关于"])
        self.menu.addMenuChild("控件", ["新建控件"])
        self.menu.addMenuChild("文档", ["控件属性"])
        self.menu.addMenuChild("关于", ["Qss编辑器"])
        self.menu.addMenuChild("关于", ["Qt样式表(官网)"])
        self.menu.connect("控件", "新建控件", self.newControl)
        self.menu.connect("关于", "Qt样式表(官网)", self.qss_official_Event)

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
    