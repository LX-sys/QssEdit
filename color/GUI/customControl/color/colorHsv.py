'''
    color_HSV
'''


from color.GUI.customControl.generalModel import *
from color.GUI.genericWidget import GenericWidget



class ColorHsv(GenericWidget):
    # 返回颜色rgba
    rgbAChange = pyqtSignal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = pyqtSignal(int)
    def __init__(self,*args):
        self._w = 255
        self._h = 20
        # 移动点的大小
        self._mouse_X = 0
        self._mouse_Y = 0
        self.ellipse_r = 5
        super(ColorHsv, self).__init__(*args)
        self.resize(self._w,self._h)

        self.maxMin()
        self.myEvent()

    def maxMin(self):
        self.setMinimumWidth(255)
        self.setMinimumHeight(20)
        self.setMaximumHeight(20)
        self.setMaximumWidth(256)

    def setUI(self):
        self.pix = QPixmap(self._w, self._h)
        self.pix.fill(Qt.transparent)
        self.createHuePixmap()
        self.img = QImage(self.pix)


    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.drawPixmap(0,0,self.pix)
        painter.drawEllipse(self._mouse_X,self._mouse_Y,
                            self.ellipse_r*2,self.ellipse_r*2)


    def _update(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        if (x >= 0 and x <= self._w-self.ellipse_r and
            y >= 0 and y <= self._h - self.ellipse_r
        ):
            self._mouse_X = x
            self._mouse_Y = y
            hsv_v = self.img.pixelColor(x, y).getHsv()[0]
            color = self.img.pixelColor(x, y).getRgb()
            self.hsvChange.emit(hsv_v)
            self.rgbAChange.emit(color)
            self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self._update(e.pos())

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self._update(e.pos())

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        i = 0.0
        gradient = QLinearGradient(256,0,0, 0)

        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        while i< 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i,1,1,1))
            i +=1.0/16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, self._w, 255)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ColorHsv()
    win.show()

    sys.exit(app.exec_())