# -*- coding:utf-8 -*-
# @time:2022/8/1512:06
# @author:LX
# @file:dynamic_control.py
# @software:PyCharm
'''
    控件工厂
'''
from PyQt5.QtWidgets import QWidget,QPushButton,QLineEdit

from core.dynamic_control import PushButton

class DynamicControl:
    def __init__(self):
        pass

    # 获取控件
    def getControl(self,control_name:str)->QWidget:
        if control_name == "QPushButton":
            return PushButton()
        elif control_name == "QLineEdit":
            return QLineEdit()
        else:
            return None