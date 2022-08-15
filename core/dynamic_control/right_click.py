# -*- coding:utf-8 -*-
# @time:2022/8/1512:16
# @author:LX
# @file:right_click.py
# @software:PyCharm

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget

# 公用右键类
class RightClick(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 注册右键
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)

    # 重命名
    def rename_Event(self):
        pass

    def menu_Event(self, pos: QPoint):
        # 创建菜单
        menu = QMenu()
        # 添加菜单项
        custom_action = menu.addAction("重命名")
        menu.addAction(custom_action)
        custom_action.triggered.connect(self.rename_Event)


        # 显示菜单
        menu.exec_(QCursor.pos())
