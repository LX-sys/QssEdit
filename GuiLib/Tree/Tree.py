# -*- coding:utf-8 -*-
# @time:2022/8/612:00
# @author:LX
# @file:Tree.py
# @software:PyCharm


import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QMenu, QInputDialog,
                             QListWidgetItem, QMessageBox, QTreeWidgetItem)


class Tree(QTreeWidget):
    filenameedit = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(Tree, self).__init__(*args, **kwargs)

        self.__structure_tree = dict()
        # 当前右键选中的节点
        self.currentItem = None  # type:QTreeWidgetItem
        # 后缀名
        self.suffix = ".qss"

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)
        self.myEvent()
        self.Init()

    def Init(self):
        self.setHeaderVisable(False)
        s = {
            "dasd":
                [
                    "301.qss", "302.qss", {
                    "ds": ["ss.qss", "sss.qss", "cc.qss"],
                    "ss": []
                }
                ],
            "hell": []
        }
        self.createTree(s)

    # 隐藏头
    def setHeaderVisable(self, visable: bool):
        self.header().setVisible(visable)

    # 创建树
    def createTree(self, tree_dict: dict, p_Item: QTreeWidgetItem = None):
        '''
        {
        "dasd":["301","302",{"ds":["ss"]}],
        }
        :return:
        '''
        # 展开
        # self.treeWidget.setItemsExpandable()
        for info, v_list in tree_dict.items():
            if p_Item is None:
                item = QTreeWidgetItem(self)
                item.setText(0, info)
            else:
                item = p_Item
                item = QTreeWidgetItem(item)
                item.setText(0, info)
            self.addTopLevelItem(item)
            for v in v_list:
                if isinstance(v, str):
                    item_c = QTreeWidgetItem(item)
                    item_c.setText(0, v)
                    self.addTopLevelItem(item_c)
                else:
                    self.createTree(v, item)

        # 结构树初始化
        self.__structure_tree = tree_dict

    # 判断节点是文件还是文件夹
    def is_folder(self, node: QTreeWidgetItem):
        if node is None:
            return None

        text = node.text(0)
        if self.suffix in text:
            return False
        return True

    # 鼠标右键创建文件夹
    def create_folder(self):
        text, ok = QInputDialog.getText(self, '创建文件夹', '请输入文件夹名称:')
        if ok:
            if text in self.__structure_tree:
                QMessageBox.warning(self, "警告", "文件夹已存在")
                return
            temp_item = None
            # 判断当前选中的节点是文件还是文件夹
            if self.is_folder(self.currentItem):
                self.currentItem.addChild(QTreeWidgetItem([text]))
                return  # 如果是文件夹，则直接返回
            else:
                if self.currentItem is None:
                    temp_item = self
                else:
                    temp_item = self.currentItem.parent()
            item = QTreeWidgetItem(temp_item)
            item.setText(0, text)
            self.addTopLevelItem(item)

    # 新建文件
    def create_file(self):
        text, ok = QInputDialog.getText(self, '创建文件', '请输入文件名称:')
        if ok:
            temp_item = None
            if self.is_folder(self.currentItem):
                temp_item = self.currentItem
            else:
                if self.currentItem is None:  # 当前没有选中的节点
                    temp_item = self
                else:
                    temp_item = self.currentItem.parent()
            item = QTreeWidgetItem(temp_item)
            item.setText(0, text + self.suffix)
            self.addTopLevelItem(item)
            # print(self.__structure_tree)

    def menu_Event(self, pos: QPoint):
        # 当前右键选中的节点
        self.currentItem = self.itemAt(pos)
        # 创建菜单
        menu = QMenu()
        # 添加菜单项
        look_action = menu.addAction("查看信息")
        menu.addAction(look_action)

        c_file_action = menu.addAction("创建文件")
        menu.addAction(look_action)
        c_file_action.triggered.connect(self.create_file)

        c_file_action = menu.addAction("创建文件夹")
        menu.addAction(look_action)
        c_file_action.triggered.connect(self.create_folder)

        # 显示菜单
        menu.exec_(QCursor.pos())

    # 双击节点事件
    def doubleClickedEvent(self, index: QModelIndex):
        # 双击对qss文件有效
        text = index.data()
        if self.suffix in text:
            # 发送信息
            self.filenameedit.emit(text)

    def myEvent(self):
        self.doubleClicked.connect(self.doubleClickedEvent)


if __name__ == '__main__':
    # 测试
    app = QApplication(sys.argv)
    tree = Tree()
    tree.show()
    sys.exit(app.exec_())
