# -*- coding:utf-8 -*-
# @time:2022/8/1114:19
# @author:LX
# @file:edit.py
# @software:PyCharm
'''

    https://www.riverbankcomputing.com/static/Docs/QScintilla/classQsciScintilla.html
    # 这个需要单独安装
    pip install QScintilla
'''


# pyqt版 - 开源代码编辑器
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QColor, QCursor,QFont
from PyQt5.QtWidgets import QApplication, QMenu,QColorDialog,QFontDialog
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs,QsciLexerCSS

from Lib import ControlLib,showControl
from color import PlateDialog,GradientDialog

class Edit(QsciScintilla):
    def __init__(self,lexer,keyword:list=None,*args,**kwargs):
        super(Edit, self).__init__(*args,**kwargs)
        # 设置python语法高亮
        self.lexer = lexer()
        self.setLexer(self.lexer)
        self.__api = QsciAPIs(self.lexer)


        # 设置代码补全
        for i in keyword:
            self.__api.add(i)
        self.__api.prepare()
        self.autoCompleteFromAll()
        self.setAutoCompletionSource(QsciScintilla.AcsAll)  # 自动补全所以地方出现的
        self.setAutoCompletionCaseSensitivity(True)  # 设置自动补全大小写敏感
        self.setAutoCompletionThreshold(1)  # 输入1个字符，就出现自动补全 提示

        # 支持中文
        self.setUtf8(True)

        # 设置编辑框的字体
        self.setFont(QFont("微软雅黑", 18))

        # 大小写不敏感
        self.setAutoCompletionCaseSensitivity(False)

        self.setEolMode(QsciScintilla.SC_EOL_CRLF) # 设置换行符为 \r\n
        self.setBraceMatching(QsciScintilla.StrictBraceMatch) # 设置括号匹配

        # 设置折叠
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)


        # 设置tab
        self.setTabWidth(4)

        # 行号设置
        self.setMarginsFont(QtGui.QFont("Consolas", 13)) # 设置行号字体
        self.setMarginType(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(0,"0000") # 行号占用宽度
        self.setMarkerForegroundColor(QColor("#ee1111"), 1)

        # 光标颜色
        self.setCaretWidth(2) # 光标宽度
        self.setCaretForegroundColor(QColor("darkCyan")) # 光标颜色
        self.setCaretLineVisible(True)  # 是否高亮显示光标所在行
        self.setCaretLineBackgroundColor(QColor(255,252,207)) # 高亮显示光标所在行的颜色

        # 设置文档窗口的标题
        # self.setWindowTitle()
        # 将槽函数链接到文本改动的信号
        self.textChanged.connect(self.textChanged_Event)
        # 给文档窗口添加右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)  #
        self.customContextMenuRequested.connect(self.RightMenu)



        self.Init()
    def textChanged_Event(self):
        pass

    def RightMenu(self,pos):
        self.menu = QMenu()
        look_action = self.menu.addAction("find")
        # look_action.triggered.connect(self.look_Action)
        del_action = self.menu.addAction("del")
        # del_action.triggered.connect(self.del_Action)
        self.menu.exec_(QCursor.pos())

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(e)

    def Init(self):
        pass



class PythonEdit(Edit):
    def __init__(self,*args, **kwargs,):
        super(PythonEdit, self).__init__(QsciLexerPython,*args, **kwargs)


    def textChanged_Event(self):
        print(self.text())

class QSSEdit(Edit):
    def __init__(self,*args, **kwargs,):
        # keyword = ["QPushButton","QLineEdit","QWidget","color","font","background-color","solid",
        #            "border-radius","border-width","border-style","border-color","hover","pressed"]
        keyword = ControlLib.controls_list()
        super(QSSEdit, self).__init__(QsciLexerCSS,keyword,*args, **kwargs)
    #     self.plate = PlateDialog()
    #     self.plate.rgbaChange.connect(self.plate_Event)
    #     # self.plate.rgbaChanged[tuple].connect(self.plate_Event)
    #
    # def plate_Event(self,color):
    #     rgba = "rgba({}, {}, {},{})".format(color[0],color[1],color[2],color[3])
    #     rgba_len = len(rgba)
    #     print(rgba)
    #     self.insert(rgba)
    #     pos = self.getCursorPosition()
    #     self.setCursorPosition(pos[0],pos[1]+rgba_len)

    def color_Event(self):
        color = QColorDialog.getColor()

        # 文字长度
        color_len = len(color.name())
        self.insert(color.name())
        pos = self.getCursorPosition()
        self.setCursorPosition(pos[0],pos[1]+color_len)

    def font_Event(self):
        font,ok = QFontDialog.getFont()
        if not ok:
            return
        # 暂时不考虑粗体
        f_ = "{}pt \"{}\"".format(font.pointSize(),font.family())
        # 文字长度
        font_len = len(f_)
        self.insert(f_)
        pos = self.getCursorPosition()
        self.setCursorPosition(pos[0],pos[1]+font_len)

    def RightMenu(self,pos):
        self.menu = QMenu()
        color_action = self.menu.addAction("颜色")
        color_action.triggered.connect(self.color_Event)
        font_action = self.menu.addAction("字体")
        font_action.triggered.connect(self.font_Event)
        self.menu.exec_(QCursor.pos())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = QSSEdit()
    edit.show()
    sys.exit(app.exec_())