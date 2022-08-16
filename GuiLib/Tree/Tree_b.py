# -*- coding:utf-8 -*-
# @time:2022/8/1618:40
# @author:LX
# @file:Tree_b.py
# @software:PyCharm
# -*- coding:utf-8 -*-
# @time:2022/8/612:00
# @author:LX
# @file:Tree.py
# @software:PyCharm

import copy
import sys,os
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QMouseEvent, QCursor,QIcon
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QMenu, QInputDialog,
                             QListWidgetItem, QMessageBox, QTreeWidgetItem)

# 路径
RootPath = os.path.abspath(os.path.dirname(__file__))
icon_Path = os.path.join(RootPath, "icon")


class Tree(QTreeWidget):
    filenameedit = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(Tree, self).__init__(*args, **kwargs)
        # default这是一个特殊的key,用于存储在最外层的.qss文件
        self.__structure_tree = {"default":[]}
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
        # s = {
        #     "dasd":
        #         [
        #             "301.qss", "302.qss", {
        #             "ds": ["ss.qss", "sss.qss", "cc.qss"],
        #             "ss": []
        #         }
        #         ],
        #     "hell": []
        # }
        s={"aa":["cc.qss",{"cc":["ll.qss"]}]}
        self.createTree(s)
        # s = {"aa": ["ss"]}
        # self.createTree(s)

    def tree(self)->dict:
        return self.__structure_tree

    # 隐藏头
    def setHeaderVisable(self, visable: bool):
        self.header().setVisible(visable)

    # 默认图标
    def get_default_icon(self)->QIcon:
        icon = QIcon()
        icon.addFile(os.path.join(icon_Path, "folder.png"), QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_open.png"), QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(os.path.join(icon_Path, "folder_av.png"), QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_av_open.png"), QSize(), QIcon.Selected, QIcon.On)
        return icon

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
                item.setIcon(0, self.get_default_icon())
                if info not in self.__structure_tree:
                    item.setText(0, info)
                else:
                    raise Exception("文件夹已存在")
            else:
                item = p_Item
                item = QTreeWidgetItem(item)
                item.setIcon(0, self.get_default_icon())
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

    # 判断是否有name的文件夹
    def is_have_folder(self,parent_name:str=None,name:str=None):
        '''
        {
            "aa":[
            "q.qss",
            {
                "bb":["q.qss","b.qss"]
            }
            ]
            "bb":[
            "q.qss",
            {
                "bb":["q.qss","b.qss"]
            }
            ]
        }
        :param parent_name: 父级文件夹名称
        :param name: 目标文件夹名称
        :return:
        '''
        if parent_name is None:
            if name in self.tree().keys():
                return True

        # for k,v in self.tree().keys():


    # 添加文件夹
    def add_folder(self,parent=None,name=""):
        if parent is None:
            parent = self
        item = QTreeWidgetItem(parent)
        item.setIcon(0, self.get_default_icon())
        item.setText(0, name)
        self.addTopLevelItem(item)

    # 将文件夹添加到树结构中去
    def __insert_folder(self,currentItem:QTreeWidgetItem,name:str):
        r_path = self.right_path(self.currentItem)
        tr_path = self.get_tree_list(self.currentItem)

        if not r_path:
            self.tree()[r_path["click"]].append(name)

        temp = self.tree()
        for i in r_path:
            temp= temp[i]
        temp.append(name)
        print(temp)

    # 鼠标右键创建文件夹
    def create_folder(self):
        text, ok = QInputDialog.getText(self, '创建文件夹', '请输入文件夹名称:')
        if ok:

            if self.currentItem is None or self.currentItem.parent() is None: # 当前没有选中的节点
                if text in self.__structure_tree: # 判断最外层是否有该文件夹
                    QMessageBox.warning(self, "警告", "文件夹已存在")
                    return
                temp_item = self
            else:
                temp_item = self.currentItem.parent()
            # 判断当前选中的节点是文件还是文件夹
            if self.is_folder(self.currentItem):
                item = QTreeWidgetItem([text])
                item.setIcon(0, self.get_default_icon())
                self.currentItem.addChild(item)
                self.right_path_address(self.currentItem).append({text:[]})
                print(self.tree())
                return  # 如果是文件夹，则直接返回


            item = QTreeWidgetItem(temp_item)
            item.setIcon(0, self.get_default_icon())
            item.setText(0, text)
            self.addTopLevelItem(item)
            if temp_item is self: # 没有选择节点的情况
                self.tree()[text] = []
            else:
                self.right_path_address(temp_item).append({text: []})
            print(self.tree())

    # 新建文件
    def create_file(self):
        text, ok = QInputDialog.getText(self, '创建文件', '请输入文件名称:')
        if ok:
            # 文件名
            qss_name = text + self.suffix

            if self.is_folder(self.currentItem):
                temp_item = self.currentItem
            elif self.currentItem is None:  # 当前没有选中的节点
                temp_item = self
            else:
                temp_item = self.currentItem.parent()
            item = QTreeWidgetItem(temp_item)
            item.setText(0, qss_name)
            self.addTopLevelItem(item)

            if temp_item is self:
                if not self.tree().get("default",None):
                    self.tree()["default"] = []
                self.tree()["default"].append(qss_name)
            else:
                # print(temp_item.text(0))
                print(temp_item)
                # print(self.right_path_address())
                print(self.right_path_address(temp_item))
                # self.right_path_address(temp_item).append(qss_name)
        print(self.tree())

    # 删除文件夹/文件
    def delete(self):
        if self.currentItem is None:
            print("没有选中的节点")
            return

        # 顶级目录
        if self.currentItem.parent() is None:
            file_name = self.currentItem.text(0)
            if self.suffix in file_name: # 如果是.qss文件
                self.tree()["default"].remove(file_name)
                self.takeTopLevelItem(self.currentIndex().row())
                return
            else:
                self.tree().pop(file_name)
                self.takeTopLevelItem(self.currentIndex().row())
                return # 如果是文件夹，则直接返回

        file_name = self.currentItem.text(0)
        if self.is_folder(self.currentItem):
            if self.currentItem.childCount() > 0:
                QMessageBox.warning(self, "警告", "该文件夹不为空,确认删除?")
                # 删除结构树中的文件夹/文件
                temp = self.right_path_address(self.currentItem.parent())
                for v in temp:
                    if isinstance(v,dict):
                        if list(v.keys())[0] == file_name:
                            temp.remove(v)
                            break
                self.currentItem.parent().removeChild(self.currentItem)
                return
        else:
            # 文件的删除
            temp = self.right_path_address(self.currentItem.parent())
            temp.remove(file_name)
            self.currentItem.parent().removeChild(self.currentItem)
        print(self.tree())

    # 鼠标右键的路径
    def right_path(self,currentItem:QTreeWidgetItem)->list:
        # 处理最外层
        if currentItem is None:
            return []
        if currentItem.parent() is None:
            return [currentItem.text(0)]

        # 路径跟踪列表
        path_track_list = []
        item = currentItem
        while item:
            p = item.parent()
            if p is not None:
                path_track_list.append(p.text(0))
            item = p
        # 反转
        path_track_list.reverse()

        # 如果点击的文件夹,则添加该文件夹名称
        if self.is_folder(currentItem):
            path_track_list.append(currentItem.text(0))

        return path_track_list

    # 根据右键路径,返回该空间的地址
    def right_path_address(self,currentItem:QTreeWidgetItem)->list:
        if currentItem is None:
            return []
        # --文件夹中添加文件夹有BUG
        path = self.right_path(currentItem)
        temp_tree = self.tree()
        temp = None
        if len(path) == 1:
            return self.tree()[path[0]]

        if self.is_folder(currentItem):
            for v in path:
                temp = temp_tree[v]
                for i in temp:
                    if isinstance(i,dict):
                        temp_tree = i
                        break
        else:
            for v in path:
                temp = temp_tree[v]
                break

        return temp

    # 获取文件夹下的文件列表
    def get_tree_list(self,currentItem:QTreeWidgetItem)->dict:

        file_names = {"file":[],"folder":[],"click":""} # 文件列表，文件夹列表，点击的节点名称
        if currentItem is None:
            return dict()

        # 文件
        if not self.is_folder(currentItem):
            if currentItem.parent() is None:
                return file_names
            else:
                currentItem = currentItem.parent()

        file_names["click"] = currentItem.text(0)

        for i in range(currentItem.childCount()):
            text = currentItem.child(i).text(0)
            if self.suffix in text:
                file_names["file"].append(text)
            else:
                file_names["folder"].append(text)
        return file_names

    def menu_Event(self, pos: QPoint):
        # 当前右键选中的节点
        self.currentItem = self.itemAt(pos)
        # 创建菜单
        menu = QMenu()
        # 添加菜单项
        look_action = menu.addAction("重命名")
        menu.addAction(look_action)

        c_file_action = menu.addAction("创建文件")
        menu.addAction(look_action)
        c_file_action.triggered.connect(self.create_file)

        c_file_action = menu.addAction("创建文件夹")
        menu.addAction(look_action)
        c_file_action.triggered.connect(self.create_folder)

        c_del_action = menu.addAction("删除")
        menu.addAction(look_action)
        c_del_action.triggered.connect(self.delete)

        # 显示菜单
        menu.exec_(QCursor.pos())

    # 双击节点事件
    def doubleClickedEvent(self, index: QModelIndex):
        # 双击对qss文件有效
        text = index.data()
        if self.suffix in text:
            print(text)
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
