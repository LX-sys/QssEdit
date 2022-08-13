'''

    颜色对话框,QWidget (继承了自定义滚动条)
'''


from color.GUI.genericWidget import GenericWidget,GenericMainWindow
from color.GUI.customControl.color.mySliderFrame import MySliderFrame
from color.GUI.customControl.generalModel import *

KEY_CENTER = 16777220

class ColorDialogSlider(MySliderFrame):
    def __init__(self, *args, **kwargs):
        super(ColorDialogSlider, self).__init__(*args, **kwargs)
    
    def myDrawBackground(self,painter:QPainter,*args,**kwargs) ->None:
        # 线性变化
        width = self.width()
        height = self.height()

        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0.0, self.getStartColor())
        gradient.setColorAt(1.0, self.getEndColor())
        painter.setBrush(gradient)
        # 绘制矩形
        painter.drawRect(0, 0, width, height)


class myQSpinBox(QSpinBox):
    '''
        增加回车信号
    '''
    returnChange = pyqtSignal(int)

    def __init__(self,*args,**kwargs):
        super(myQSpinBox, self).__init__(*args,**kwargs)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == KEY_CENTER:
            v = self.value()
            if v:
                self.returnChange.emit(v)
            else:
                self.setValue(0)
                self.returnChange.emit(0)

        QSpinBox.keyPressEvent(self,e)


# GRB颜色对话框
class RGBDialog(GenericWidget):
    # 当颜色变化时触发信号
    rgbChange = pyqtSignal(tuple)  # RGB事件
    rGbaChange = pyqtSignal(tuple) # rGBa事件

    def __init__(self,*args,**kwargs):
        self._r = 0
        self._g = 0
        self._b = 0
        # 透明度
        self._alpha = 255
        '''
            透明度0-255
            但是显示界面是0-100
            100/255 等于 self._alpha_t
            滚轮当前数值/self._alpha_t 就等于0-255区间度值
        '''
        self._alpha_t = 100.0 / RGBMAX_VALUE  # 透明度 100化

        super(RGBDialog, self).__init__(*args,**kwargs)
        self.setMinimumHeight(100)
        self.myEvent()

    def _spinbox(self,box_obj):
        box_obj.setMaximum(255)
        box_obj.setMaximumWidth(55)
        box_obj.setMaximumHeight(20)

    def setUI(self):
        # 网格布局
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.slider_red = ColorDialogSlider()
        self.slider_red.setObjectName("slider_red")
        self.slider_red.move(0, 0)
        self.slider_red.setEndColor(QColor("red"))
        self.spinBox_red = myQSpinBox()
        self._spinbox(self.spinBox_red)
        self.gridLayout.addWidget(self.slider_red,0,0,1,1)
        self.gridLayout.addWidget(self.spinBox_red,0,1,1,1)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(horizontalSpacer,0,2,1,1)

        self.slider_green = ColorDialogSlider()
        self.setObjectName("slider_green")
        self.slider_green.move(0, 26)
        self.slider_green.setEndColor(QColor("green"))
        self.spinBox_green = QSpinBox()
        self._spinbox(self.spinBox_green)
        self.gridLayout.addWidget(self.slider_green, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.spinBox_green, 1, 1, 1, 1)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(horizontalSpacer, 1, 2, 1, 1)

        self.slider_blue = ColorDialogSlider()
        self.setObjectName("slider_blue")
        self.slider_blue.move(0, 52)
        self.slider_blue.setEndColor(QColor("blue"))
        self.spinBox_blue = QSpinBox()
        self._spinbox(self.spinBox_blue)
        self.gridLayout.addWidget(self.slider_blue, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.spinBox_blue, 2, 1, 1, 1)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(horizontalSpacer, 2, 2, 1, 1)

        # 透明度
        self.slider = QSlider()
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setOrientation(Qt.Horizontal)
        self.spinBox_slider = QSpinBox()
        self._spinbox(self.spinBox_slider)
        self.spinBox_slider.setMaximum(100)
        self.spinBox_slider.setValue(self.slider.value())
        self.gridLayout.addWidget(self.slider, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.spinBox_slider, 3, 1, 1, 1)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(horizontalSpacer, 3, 2, 1, 1)

        # 颜色展示标签
        self.bel = QLabel()
        self.bel.resize(40,40)
        self.bel.setStyleSheet("background-color: rgba({}, {}, {},{})".format(self._r,
                                                                              self._g,
                                                                              self._b,
                                                                              self._alpha))
        self.bel.setMinimumSize(QSize(40,40))
        self.bel.setMaximumSize(QSize(40,40))
        self.gridLayout.addWidget(self.bel, 4, 0, 1, 1)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(verticalSpacer,4,1,1,1)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(verticalSpacer, 5, 0, 1, 1)

        self.myEvent()


    def myEvent(self):
        # 三原色事件
        self.slider_red.sliderChange[int].connect(self._red)
        self.slider_green.sliderChange[int].connect(self._green)
        self.slider_blue.sliderChange[int].connect(self._blue)
        '''
            valueChanged事件
            注意上面三个事件和下面三个事件,在鼠标移动方块时时会同时触发,
            也就是说 move会被执行两次,但是肉眼看不出区别. 消耗时间长，但是体验更流畅
            
            returnChange
            如果使用这个事件,move只会执行一次,但是在修改rgb值的时候,会有会车时才会生效
        '''
        self.spinBox_red.valueChanged[int].connect(self._spinBox_red)
        self.spinBox_green.valueChanged[int].connect(self._spinBox_green)
        self.spinBox_blue.valueChanged[int].connect(self._spinBox_blue)

        # 透明度
        self.slider.valueChanged[int].connect(self._slider)
        self.spinBox_slider.valueChanged[int].connect(self._spinBox_slider)

    def rgb(self):
        return self._r,self._g,self._b

    # 带透明度
    def rGba(self):
        return self._r, self._g, self._b, self._alpha

    # 除自己以外的两种颜色渐变
    def colorTwo(self,slider_obj:QSlider):
        gradient_color = {"slider_red": {"obj":self.slider_red,
                                         "s":QColor(0, self._g, self._b, self._alpha),
                                         "e":QColor(255, self._g, self._b, self._alpha)
                                        },
                           "slider_green": {"obj":self.slider_green,
                                            "s":QColor(self._r, 0, self._b, self._alpha),
                                            "e":QColor(self._r, 255, self._b, self._alpha)
                                           },
                           "slider_blue": {"obj":self.slider_blue,
                                           "s":QColor(self._r, self._g, 0, self._alpha),
                                           "e":QColor(self._r, self._g, 255, self._alpha)
                                          }
                           }

        # 执行除了自己以外的两种颜色
        for obj_k,color_v in gradient_color.items():
            if slider_obj.objectName() != obj_k:
                startColor = gradient_color[obj_k]["s"]
                endColor = gradient_color[obj_k]["e"]
                gradient_color[obj_k]["obj"].setLinearGradient(startColor,endColor)

    # 颜色展示
    def _colorShow(self):
        self.bel.setStyleSheet("background-color: rgba({}, {}, {},{});".format(*self.rGba()))

    # 发送信号
    def _change(self):
        self.rgbChange.emit(self.rgb())
        self.rGbaChange.emit(self.rGba())
        self._colorShow()


    def _red(self,r_v:int):
        self._r = r_v
        self._change()
        self.colorTwo(self.slider_red)
        self.spinBox_red.setValue(r_v)

    def _green(self,g_v:int):
        self._g = g_v
        self._change()
        self.colorTwo(self.slider_green)
        self.spinBox_green.setValue(g_v)

    def _blue(self,b_v:int):
        self._b = b_v
        self._change()
        self.colorTwo(self.slider_blue)
        self.spinBox_blue.setValue(b_v)

    def _spinBox_red(self,v):
        # 颜色,位置 同步
        self._red(v)
        self.slider_red.setPos(v)

    def _spinBox_green(self,v):
        self._green(v)
        self.slider_green.setPos(v)

    def _spinBox_blue(self,v):
        self._blue(v)
        self.slider_blue.setPos(v)

    def _getVdivAlpha(self,v:float) -> int:
        return int(v//self._alpha_t)

    # 透明度事件
    def _slider(self,v):
        self.spinBox_slider.setValue(v)
        self._alpha = self._getVdivAlpha(v)
        self.rGbaChange.emit(self.rGba())
        self._colorShow()

    def _spinBox_slider(self,v):
        self.slider.setValue(v)
        self._alpha = self._getVdivAlpha(v)
        self.rGbaChange.emit(self.rGba())
        self._colorShow()


# --------------测试

class Test(GenericMainWindow):
    # 颜色改变信号信号
    GradientChange = pyqtSignal()

    def __init__(self):
        super(Test, self).__init__()

        self.setWindowTitle("颜色渐变对话框")
        self.resize(500,500)
        self.move(0,0)

    def setUI(self):

        self.ss = RGBDialog(self)
        self.ss.move(20, 20)
        self.ss.resize(400, 300)
        self.ss.rGbaChange[tuple].connect(self.test)

    def test(self,t):
        print("t->",t)

    def myEvent(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    sys.exit(app.exec_())