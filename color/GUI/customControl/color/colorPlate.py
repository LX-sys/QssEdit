'''

    色版,色版对话框
'''

from color.GUI.genericWidget import *
from color.GUI.customControl.generalModel import *
from color.GUI.customControl.color.colorHsv import ColorHsv


# 色版
class ColorPlate(GenericWidget):
    rgbaChange = pyqtSignal(tuple)

    def __init__(self,*args,**kwargs):
        # h 色调值  s  v
        self.tonal_value = 350
        self.s_value = 255
        self.v_value = 255
        # 图像位置
        self._pPos_x = 10
        self._pPos_y = 40

        # 移动圆圈的大小
        self._mouse_X = 0
        self._mouse_Y = 0
        self.ellipse_r = 8  # 半径
        self._mouse_color = Qt.white  # 圆圈颜色
        
        # 透明度
        self._alpha = 255

        # 当前颜色值
        self._RGBA = [255,255,255,255]
        # 颜色的十六进制
        self._colorHex = ""

        super(ColorPlate, self).__init__(*args,**kwargs)
        # self.resize(383,339)
        self.setMinimumSize(383,339)
        self.setMaximumSize(383,339)
        self.myEvent()

    def setHub(self,h):
        self.tonal_value = h
        self.updatePreview()
        self.update()

    def setUI(self):
        # HSV颜色标签
        self.hsv = ColorHsv(self)
        self.hsv.move(self._pPos_x,10)

        self.alpha_bel = QLabel("透明度:",self)
        self.alpha_bel.move(10,305)
        self.percentage_bel = QLabel("100%",self)
        self.percentage_bel.move(240,305)

        # 滑块
        self.alpha = QSlider(self)
        self.alpha.setOrientation(Qt.Horizontal)
        self.alpha.move(self._pPos_x+50,300)
        self.alpha.resize(255-50-30,30)
        self.alpha.setMaximum(100)
        self.alpha.setValue(100)

        #
        self.R_bel = QLabel("红(R)",self)
        self.G_bel = QLabel("绿(G)",self)
        self.B_bel = QLabel("蓝(B)",self)
        self.A_bel = QLabel("透(A)",self)
        self.R_spinBox = QSpinBox(self)
        self.G_spinBox = QSpinBox(self)
        self.B_spinBox = QSpinBox(self)
        self.A_spinBox = QSpinBox(self)
        self.R_spinBox.setMaximum(255)
        self.G_spinBox.setMaximum(255)
        self.B_spinBox.setMaximum(255)
        self.A_spinBox.setMaximum(255)
        self.R_bel.move(270,40)
        self.G_bel.move(270,70)
        self.B_bel.move(270,100)
        self.A_bel.move(270,130)
        self.R_spinBox.move(310,39)
        self.G_spinBox.move(310,69)
        self.B_spinBox.move(310,99)
        self.A_spinBox.move(310,129)
        self.Hex_bel = QLabel("十 六", self)
        self.Hex_line = QLineEdit(self)
        self.Hex_line.resize(63,20)
        self.Hex_line.setReadOnly(True)
        self.Hex_bel.move(270,160)
        self.Hex_line.move(310,159)


        # --
        self.preview()
        self.createSVPixmap()
        self.updatePreview()

    def myEvent(self):
        self.hsv.hsvChange[int].connect(self._hsv)
        self.alpha.valueChanged[int].connect(self._alpha_valueChanged)

    def setSpinbox(self):
        self.R_spinBox.setValue(self._RGBA[0])
        self.G_spinBox.setValue(self._RGBA[1])
        self.B_spinBox.setValue(self._RGBA[2])
        self.A_spinBox.setValue(self._RGBA[3])
        self.Hex_line.setText(self._colorHex)

    def _alpha_valueChanged(self,v:int):
        self.percentage_bel.setText(str(v)+"%")
        # 透明度变化
        self._alpha = int(v//(100/255))
        self._RGBA[3] = self._alpha
        # 更新图像
        self.updatePreview()
        # 更新SpinBox
        self.setSpinbox()
        self.rgbaChange.emit(tuple(self._RGBA))
        self.update()

    def _hsv(self,hsv):
        self.tonal_value = hsv
        # 更新图像
        self.updatePreview()
        # 更新SpinBox
        self.setSpinbox()
        temp = (self.tonal_value,self.s_value,self.v_value)
        rgba = self._hsvToRgba(*temp)
        self.rgbaChange.emit(rgba)

        self.update()


    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        # 下面这两句的位置不能换
        painter.drawPixmap(self._pPos_x,self._pPos_y,self.pix2)
        painter.drawPixmap(self._pPos_x,self._pPos_y, self.pix)

        painter.setPen(self._mouse_color)
        painter.drawEllipse(self._mouse_X+self._pPos_x, self._mouse_Y+self._pPos_y,
                            self.ellipse_r * 2, self.ellipse_r * 2)

    def preview(self):
        self.pix = QPixmap(256,256)
        self.pix.fill(Qt.transparent)

        painter = QPainter(self.pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        gradient = QLinearGradient(0,0,0,360)
        gradient.setColorAt(0,QColor(0,0,0,0))
        gradient.setColorAt(1,QColor(0,0,0,255))

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0,0,256,256)


    def _setSV(self,s:int,v:int)->None:
        self.s_value = s
        self.v_value = v

    # hsv转成rgba
    def _hsvToRgba(self,h:int,s:int,v:int)->tuple:
        color = QColor()
        color.setHsv(h, s, v)
        # print(color.name())
        # 设置十六进制
        self._colorHex = color.name()
        self._setSV(s, v)
        self._RGBA = list(color.getRgb())
        self._RGBA[3] = self._alpha
        return tuple(self._RGBA)

    def _setMousePos(self,e: QtGui.QMouseEvent):
        '''
            检查鼠标是否点击在图像上,并设置鼠标位置
        :param e:
        :return:
        '''
        if (e.x() >= 0 + self._pPos_x and
            e.x() <= self._pPos_x + 255 - self.ellipse_r * 2 and
            e.y() >= 0 + self._pPos_y and
            e.y() <= self._pPos_y + 255 - self.ellipse_r * 2
        ):
                self._mouse_X = e.x() - self._pPos_x
                self._mouse_Y = e.y() - self._pPos_y
                self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self._setMousePos(e)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self._setMousePos(e)
        # 这里y需要减一个255,将颜色矫正,不然是反的
        x = e.pos().x()-self._pPos_x
        y = 255-e.pos().y()+self._pPos_y
        if x>=0 and x <= 255 and y>=0 and y<=255:
            rgba = self._hsvToRgba(self.tonal_value, x, y)
            # 更新SpinBox
            self.setSpinbox()
            self.rgbaChange.emit(rgba)
            self.update()

    def createSVPixmap(self):
        self.pix2 = QPixmap(256,256)
        self.pix2.fill(Qt.transparent)

    def updatePreview(self):

        color = QColor()
        color.setHsv(self.tonal_value,255,255,self._alpha)

        painter = QPainter(self.pix2)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, 360, 0)
        gradient.setColorAt(1,color)
        gradient.setColorAt(0,QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, 256, 256)

# 色版对话框
class PlateDialog(GenericMainWindow):
    rgbaChange = pyqtSignal(tuple)

    def __init__(self):
        super(PlateDialog, self).__init__()
        self.setWindowTitle("颜色编辑器")
        self.setMinimumSize(383, 339)
        self.setMaximumSize(383, 339)
        self.c = ColorPlate(self)
        self._color = None
        self.myEvent()

    def myEvent(self):
        self.c.rgbaChange[tuple].connect(self._send)

    def getRgba(self)->tuple:
        return self._color

    def _send(self, rgba: tuple):
        self._color = rgba
        self.rgbaChange.emit(rgba)


# -----测试
class Test(GenericMainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.setWindowTitle("das")
        self.resize(500,500)
        self.myEvent()


    def setUI(self):
        self.btn = QPushButton(self)
        self.btn.resize(50, 50)
        self.btn.move(400, 50)

        self.c = ColorPlate(self)
    def myEvent(self):
        self.c.rgbaChange[tuple].connect(self.test)

    def test(self,rgba:tuple):
        self.btn.setStyleSheet("background-color: rgba({}, {}, {},{});".format(*rgba))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    sys.exit(app.exec_())