

'''
    自定义滚动条窗口
'''

from color.GUI.customControl.generalModel import *
from color.GUI.genericWidget import GenericWidget

'''
    子类重写 myDrawBackground方法
'''

class MySliderFrame(GenericWidget):
    sliderChange = pyqtSignal(int)  # type:pyqtSignal

    def __init__(self,*args,**kwargs):

        self._btn_obj = None  # type:QPushButton
        super(MySliderFrame, self).__init__(*args,**kwargs)

        self.setMaximumHeight(25)
        self.setContentsMargins(0, 0, 0, 0)

        # 最小最大值
        self._minStep = RGBMIN_VALUE
        self._maxStep = RGBMAX_VALUE
        self._value = 0.0
        # 步长
        self._t = self.width() / self._maxStep

        self._startColor = QColor("black")
        self._endColor = QColor("red")

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.resize(e.size())
        # 窗口发生变化,t重新计算
        self._t = self.width() / self._maxStep

    def setMinValue(self,value:int) -> None:
        self._minStep = value

    def setMaxValue(self,value:int) -> None:
        self._maxStep = value

    def value(self) -> int:
        return int(self._value)

    def setUI(self):
        btn = QPushButton(self)
        btn.resize(MOUSE_SQUARE_W, MOUSE_SQUARE_H)
        btn.setMaximumWidth(MOUSE_SQUARE_W)
        btn.setMaximumHeight(MOUSE_SQUARE_H)
        btn.move(0, self.height()//+14)
        self._btn_obj = btn

    # 设置轮轴位置
    def setPos(self,x:int):
        if self._btn_obj:
            '''
                已知RGB值(x)和步长,求移动距离
            '''
            self._btn_obj.move(int(x * self._t),
                               int(self.height()//+14))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Painter already active 解决方案,不使用begin(self),end()
        painter = QPainter(self)
        # painter.begin(self)
        self.myDrawBackground(painter)
        # painter.end()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if (e.buttons() == Qt.LeftButton) and self._btn_obj:
            if e.x() >=0 and e.x() <= self.width():
                self._btn_obj.move(e.x(),self._btn_obj.y())
                '''
                    已知移动距离和步长,求RGB值
                '''
                self._value = int(e.x()/self._t)
                self.sliderChange.emit(self._value)


    # 设置线性渐变的开始
    def setStartColor(self,color:QColor):
        self._startColor = color

    # ...末尾值
    def setEndColor(self,color:QColor):
        self._endColor = color

    def getStartColor(self) -> QColor:
        return self._startColor

    def getEndColor(self) -> QColor:
        return self._endColor

    # 设置线性变化的开始颜色与末尾颜色
    def setLinearGradient(self,statColor:QColor,endColor:QColor):
        self.setStartColor(statColor)
        self.setEndColor(endColor)
        self.update()

    # 绘制背景
    def myDrawBackground(self,painter:QPainter,*args,**kwargs)->None:
        pass
        # width = painter.device().width()
        # height = painter.device().height()
        #
        # # 线性变化
        # gradient = QLinearGradient(0,0,width,height)
        # gradient.setColorAt(0.0,self._startColor)
        # gradient.setColorAt(1.0,self._endColor)
        # painter.setBrush(gradient)
        # # 绘制矩形
        # painter.drawRect(0,0,width,height)