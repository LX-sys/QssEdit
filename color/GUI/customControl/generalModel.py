'''

    GUI 公用库
'''


import re
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QSize,QPoint
from PyQt5.QtGui import (QPainter, QColor,QLinearGradient,QRadialGradient,QGradient,QConicalGradient,
                         QGradient,QPixmap,QBrush,QImage,QMouseEvent,QCursor,QFont, QFontMetrics)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QSlider,QLabel,QMenu,QFrame,
QGridLayout, QSpinBox, QSpacerItem, QSizePolicy,QMainWindow,QVBoxLayout,QLineEdit)
# from color.GUI.customControl.publicKeys import *
# from qtwidgets import Gradient

# 可移动方块的w,h
MOUSE_SQUARE_W = 18
MOUSE_SQUARE_H = 18

# grb最值
RGBMIN_VALUE = 0.0
RGBMAX_VALUE = 255.0