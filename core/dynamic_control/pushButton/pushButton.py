# -*- coding:utf-8 -*-
# @time:2022/8/1512:11
# @author:LX
# @file:pushButton.py
# @software:PyCharm
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton

from core.dynamic_control.right_click import RightClick


# 按钮
class PushButton(QPushButton,RightClick):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText("btn")

    def rename_Event(self):
        print("当前名称:" + self.text())
        print("重命名为:hello")
        self.setText("hello")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    button = PushButton()
    button.show()
    sys.exit(app.exec_())