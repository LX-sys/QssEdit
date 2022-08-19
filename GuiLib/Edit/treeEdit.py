# -*- coding:utf-8 -*-
# @time:2022/8/1811:12
# @author:LX
# @file:treeEdit.py
# @software:PyCharm
'''
    带目录和tab的编译器

'''

import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor, QCursor,QFont
from PyQt5.QtWidgets import QApplication, QMenu,QWidget,QGridLayout,QSplitter,QTreeWidgetItem


# from Edit.edit import QSSEdit
# from Tab.tab import Tab
# from Tree.Tree import Tree

from GuiLib.Edit.edit import QSSEdit
from GuiLib.Tab.tab import Tab
from GuiLib.Tree.Tree import Tree


class TreeEdit(QWidget):
    treeRightClicked = pyqtSignal()
    treeLeftClicked = pyqtSignal(str)
    switchTab = pyqtSignal(int)

    def __init__(self,*args,**kwargs):
        super(TreeEdit, self).__init__(*args,**kwargs)

        # 网格布局,水平分裂器
        self.gbox = QGridLayout(self)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.gbox.addWidget(self.splitter)

        # 树,tab
        self.tree = Tree(self.splitter)
        self.tab = Tab(self.splitter)


        # 初始化
        self.Init()
        # 事件初始化
        self.myEvent()


    def createTreeFile(self,name:str):
        return self.tree.create_file(name)

    def setCloseMouseRight(self,b:bool=True):
        self.tree.setCloseMouseRight(b)

    def closeMouseRight(self)->bool:
        return self.tree.closeMouseRight()

    def Init(self):
        self.setCloseMouseRight(True)

        # 调整布局
        tree_w = int(self.width()*0.25)
        self.splitter.setSizes([tree_w,self.width()-tree_w])

    def addTab(self,widget:QWidget, name: str):
        self.tab.addTab(widget, self.fullPath(name))

    # 合成完整路径
    def fullPath(self,name)->str:
        if self.tree.suffix in name:
            return self.tree.fullPath(self.tree.currentItem)+"/"+name
        return self.tree.fullPath(self.tree.currentItem) + "/" + name + self.tree.suffix

    # 添加
    def add(self,name:str=None):
        if self.closeMouseRight():
            self.tab.addTab(QSSEdit(),name)
        else:
            print("没有名字")
            # 发送信号-新建文件
            self.treeRightClicked.emit()

        # self.tree.create_file(name)

    def delete_file(self,name:str):
        print("delete_file",name)
        self.tab.delete(name)

    # 点击树打开tab
    def open_tab(self,name:str):
        self.tab.setTabState(name,True)
        self.focusTab(name)

    def getCurrentTab(self,index)->str:
        return self.tab.tabText(index)

    # 切换tab
    def changeTabed(self,index:int):
        self.switchTab.emit(index)

    def is_tab(self,name:str)->bool:
        return self.tab.is_tab(name)

    def focusTab(self,name:str):
        self.tab.focusTab(name)

    # 树左键信号
    def left_click_Event(self,item:QTreeWidgetItem):
        self.treeLeftClicked.emit(self.fullPath(item.text(0)))

    def myEvent(self):
        self.tree.rightClickFile.connect(self.add)
        self.tree.rightClicked.connect(self.add)
        self.tree.leftClicked.connect(self.left_click_Event)
        self.tree.delefile.connect(self.delete_file)
        self.tree.filenameedit.connect(self.open_tab)
        self.tab.tabBarClicked.connect(self.changeTabed)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TreeEdit()
    win.show()

    sys.exit(app.exec_())
