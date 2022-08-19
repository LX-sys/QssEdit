# -*- coding:utf-8 -*-
# @time:2022/8/1318:18
# @author:LX
# @file:controlshell.py
# @software:PyCharm


from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtWidgets import QPushButton,QFrame,QWidget,QGridLayout,QLineEdit

from core.dynamic_control import PushButton

# 控件外壳
class ControlShell(QFrame):
    objed = pyqtSignal(dict)

    def __init__(self,control_name=None,alias:str=None,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 鼠标移动标记
        self.m_flag = False
        self.m_Position = QPoint(0,0)

        # 控件名称,和别名
        self.__control_name = (control_name,alias)
        self.__obj = {"self":self}

        self.gridLayout = QGridLayout(self)
        self.setObjectName("ABC")

        if control_name and alias:
            if type(control_name) == str:
                self.createControl(control_name,alias)
            else:
                self.createControl(widget=control_name,alias=alias)

    def activate(self,b:bool):
        old_style = self.styleSheet()
        if b:
            self.setStyleSheet(old_style+'''\n
            QFrame#ABC{
            border:1px solid rgb(0, 0, 255);
            }
            ''')
        else:
            self.setStyleSheet(old_style+'''\n
                        QFrame#ABC{
                        border:1px solid gray;
                        }
                        ''')

    def name(self)->tuple:
        return self.__control_name

    # 当前控件对象
    def getObj(self)->QWidget:
        return self.__obj[self.name()[0]][0][self.name()[0]]

    def getSelf(self)->QWidget:
        return self

    def createControl(self,name:str="test",alias:str=None,widget:QWidget=None):
        if widget is None:
            if name == "QPushButton":
                widget = PushButton(self)

            if name == "QLineEdit":
                widget = QLineEdit(self)
                widget.resize(100,30)

        if widget:
            if widget not in self.__obj:
                self.__obj[name] = [{name:widget,"alias":alias}]
            else:
                self.__obj[name].append({name:widget,"alias":alias})
            self.gridLayout.addWidget(widget)
            print(self.__obj)

    def is_successful(self)->bool:
        if len(self.__obj) == 1:
            return False
        return True

    # 拖动窗口
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtCore.Qt.ClosedHandCursor)#更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)#更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtCore.Qt.ArrowCursor)


# 控件群
class ControlGroup:
    def __init__(self):
        '''
        {
            控件名称: [控件外壳,控件外壳,控件外壳]
        }

        '''
        self.__group = dict()
        self.curr_activate_control = None

    # 设置控件外壳为激活状态,其他控件外壳设置为非激活状态
    def setActivateControl(self,name:str,alias:str=None):
        if name not in self.controlGroup():
            return
        print("--asd")
        c_list = self.getControlList(name)
        for c in c_list:
            if c["alias"] == alias:
                self.curr_activate_control = c["control"]
                c["control"].activate(True)
            else:
                c["control"].activate(False)
        print("激活完成")

    def controlGroup(self)->dict:
        return self.__group

    # 获取当前的激活的控件
    def getActivateControl(self)->ControlShell:
        return self.curr_activate_control

    # 添加控件外壳
    def addControlShell(self,control_shell:ControlShell):
        name,alias = control_shell.name()
        if self.is_alias(name,alias):
            return
            # raise Exception("别名重复")

        if name not in self.controlGroup():
            self.controlGroup()[name] = [{"control":control_shell,"alias":alias}]
        else:
            self.controlGroup()[name].append({"control":control_shell,"alias":alias})


    # 判断相同控件下是否有别名重复
    def is_alias(self,name:str,alias:str)->bool:
        if name not in self.controlGroup():
            return False

        c_list = self.getControlList(name)
        for c in c_list:
            if c["alias"] == alias:
                return True
        return False

    # 获取控件列表
    def getControlList(self,name:str)->list:
        if name not in self.controlGroup():
            return []
        return self.controlGroup()[name]

    # 获取控件外壳
    def getControlShell(self,name:str,alias:str=None)->ControlShell:
        if name not in self.controlGroup():
            return None

        c_list = self.getControlList(name)
        for c in c_list:
            if c.name()[1] == alias:
                return c