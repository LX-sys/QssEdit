'''

    控件库

'''
import re


class ControlLib:
    controls ={
        "QLabel":{"QLabel":"/*标签*/",
                  "QLabel:hover":"/*鼠标放在标签上时的样式*/"
                },
        "QPushButton":{"QPushButton":"/*按钮*/",
                       "QPushButton:hover":"/*鼠标放在按钮上时的样式*/",
                       "QPushButton:pressed":"/*按钮按下时的样式*/",
                       "QPushButton::menu-indicator":"/*菜单指示器子控件(在菜单栏时的样式)*/",
                       "QPushButton:open":"/*按钮在菜单打开时的样式*/"},
        "QToolButton":{"QToolButton":"/*工具按钮*/"},
        "QRadioButton":{"QRadioButton":"/*单选框*/",
                       "QRadioButton::indicator":"/*文本旁边的标志样式/*",
                       "QRadioButton::indicator::unchecked":"/*文本旁边的标志没有选中时的样式*/",
                       "QRadioButton::indicator:unchecked:hover":"/*文本旁边的标志没有选中时的鼠标放上去时的样式*/",
                       "QRadioButton::indicator:unchecked:pressed":"/*文本旁边的标志没有选中按下时一瞬间的样式*/",
                       "QRadioButton::indicator::checked":"/*文本旁边的标志选中时的样式*/",
                       "QRadioButton::indicator:checked:hover":"/*文本旁边的标志选中时的鼠标放上去时的样式*/",
                       "QRadioButton::indicator:checked:pressed":"/*文本旁边的标志选中按下时一瞬间的样式*/"
                       },
        "QLineEdit":{"QLineEdit":"/*输入行(setEchoMode('Password')可以将输入该文密文)*/",
                     "QLineEdit[readOnly='true']":"/*只读时样式(需要将readOnly设置为真才生效)*/",
                     "QLineEdit:read-only":"/*只读时样式(需要将readOnly设置为真才生效)*/"
                     },
        "QTextEdit":{"QTextEdit":"文本编辑与QLineEdit类似"},
        "QCheckBox":{"QCheckBox":"/*复选框,将tristate设置为真时有三种状态(选中,未选中,待选中)*/",
                     "QCheckBox::indicator":"/*文本旁边的标志样式*/",
                     "QCheckBox::indicator:unchecked":"/*文本旁边的标志没有选中时的样式*/",
                     "QCheckBox::indicator:unchecked:hover":"/*文本旁边的标志没有选中时的鼠标放上去时的样式*/",
                     "QCheckBox::indicator:unchecked:pressed":"/*文本旁边的标志没有选中按下时一瞬间的样式*/",
                     "QCheckBox::indicator:checked":"/*文本旁边的标志选中时的样式*/",
                     "QCheckBox::indicator:checked:hover":"/*文本旁边的标志选中时的鼠标放上去时的样式*/",
                     "QCheckBox::indicator:checked:pressed":"/*文本旁边的标志选中按下时一瞬间的样式*/",
                     "QCheckBox::indicator:indeterminate:hover":"/*文本旁边的标志待选中时的鼠标放上去时的样式(需要将tristate设置为真才生效)*/",
                     "QCheckBox::indicator:indeterminate:pressed":"/*文本旁边的标志待选中按下时一瞬间的样式(需要将tristate设置为真才生效)*/"},
        "QComboBox":{"QComboBox":"/*下拉框*/",
                     "QComboBox:!editable": "/*编辑框样式*/",
                     "QComboBox:editable":"/*编辑框样式(需要将editable设置为真才生效,内容可编辑)*/",
                     "QComboBox::drop-down":"/*下拉按钮样式*/",
                     "QComboBox::drop-down:editable":"/*下拉按钮样式(需要将editable设置为真才生效,内容可编辑)*/",
                     "QComboBox:!editable:on": "/*拉下列表展开时,编辑框样式*/",
                     "QComboBox::drop-down:!editable:on":"/*拉下列表展开时,下拉按钮样式*/",
                     "QComboBox:on":"/*拉下列表展开时,文本的样式*/",
                     "QComboBox::down-arrow":"按钮里的图标样式",
                     "QComboBox::down-arrow:on":"/*拉下列表展开时，移动箭头*/"
                     },
        "QDockWidget":{"QDockWidget":"/*程序坞窗口(停靠窗口)*/",
                       "QDockWidget::title":"/*窗口标题样式*/",
                       "QDockWidget::close-button":"/*关闭按钮样式*/",
                       "QDockWidget::float-button":"/*浮动按钮样式*/",
                       "QDockWidget::close-button:hover":"/*鼠标放在关闭按钮上时的样式*/",
                       "QDockWidget::float-button:hover":"/**鼠标放在浮动按钮上时的样式*/",
                       "QDockWidget::close-button:pressed":"/*鼠标按下关闭按钮时的样式*/",
                       "QDockWidget::float-button:pressed":"/*鼠标按下浮动按钮时的样式*/"
                       },
        "QGroupBox":{"QGroupBox":"/*组合框(与QCheckBox样式相似)*/",
                      "QGroupBox::title":"/*标题样式*/",
                      "QGroupBox::indicator":"/*标题旁边控件样式(需要将checkable)设置为真才生效*/",
                      "QGroupBox::indicator:unchecked":"/*标题旁边控件没有选中时的样式(需要将checkable)设置为真才生效)*/"
                      },
        "QListView":{"QListView":"/*列表视图*/",
                     "QListView::item:alternate":"/**/",
                     "QListView::item:selected":"/**/",
                     "QListView::item:selected:!active":"/**/",
                     "QListView::item:selected:active":"/**/",
                     "QListView::item:hover":"/**/"
                     },
        "QMenu":{"QMenu":"/*菜单样式*/",
                 "QMenu::item":"/*菜单每一项的样式*/",
                 "QMenu::item:selected":"/*选择一项时的样式*/",
                 "QMenu::separator":"/*分隔符的样式*/",
                 "QMenu::indicator":"/**/",
                 "QMenu::icon:checked":"/**/"
                 },
        "QMenuBar":{"QMenuBar":"/*菜单栏样式*/",
                    "QMenuBar::item":"/*菜单栏每一项的样式*/",
                    "QMenuBar::item:selected":"/*选择一项时的样式*/",
                    "QMenuBar::item:pressed":"/*一项按下时的样式*/"
                    },
        "QProgressBar":{"QProgressBar":"/*进度条*/",
                        "QProgressBar::chunk":"进度条中间颜色区域样式"},
        "QScrollBar":{"QScrollBar":'''
                    /*滚动条样式
                    QScrollBar 指所有滚动条样式
                    QScrollBar:horizontal 水平
                    QScrollBar:vertical  垂直
                    */
                    ''',
                      "QScrollBar:horizontal":"/*水平滚动条样式*/",
                      "QScrollBar::handle:horizontal":"/*水平滚动条中手柄的样式*/",
                      "QScrollBar::add-line:horizontal":"/*水平滚动条最右边按钮样式*/",
                      "QScrollBar::sub-line:horizontal":"/*水平滚动条最左边按钮样式*/",
                      "QScrollBar:vertical":"/**/",
                      "QScrollBar::handle:vertical":"/**/",
                      "QScrollBar::add-line:vertical":"/**/",
                      "QScrollBar::sub-line:vertical":"/**/"},
        "QSlider":{"QSlider":
                    '''
                    /*
                    滑动条
                    QSlider 指所有滑动条
                    还有 horizontal vertical
                    */
                    ''',
                   "QSlider::groove:horizontal":"/*水平凹槽样式*/",
                   "QSlider::handle:horizontal":"/*水平手柄样式*/",
                   "QSlider::add-page:horizontal":"/*更改手柄前后滑块部分的样式*/",
                   "QSlider::sub-page:horizontal":"/*更改手柄前后滑块部分的样式*/",
                   "QSlider::groove:vertical": "/**/",
                   "QSlider::handle:vertical": "/**/",
                   "QSlider::add-page:vertical": "/**/",
                   "QSlider::sub-page:vertical": "/**/"
                   },
        "QSpinBox":{"QSpinBox":"/*微调框*/",
                    "QSpinBox::up-button":"/*上按钮样式*/",
                    "QSpinBox::up-button:hover":"鼠标放在上按钮时的样式",
                    "QSpinBox::up-button:pressed":"鼠标按下 下按钮时的样式",
                    "QSpinBox::up-arrow":"上按钮里小箭头样式",
                    "QSpinBox::down-button":"/*下按钮样式*/",
                    },
        "QDoubleSpinBox":{"QDoubleSpinBox":
                    '''
                    /*
                    样式与QSpinBox基本一样,请直接查看QSpinBox样式
                    */
                    '''},
        "QSplitter":{"QSplitter":
                     '''
                     /*
                     不是控件,是属于布局管理器的一种
                     分割器
                     */
                     ''',
                     "QSplitter::handle":"/*手柄样式,建议设置image属性*/",
                     "QSplitter::handle:horizontal":"/*水平手柄样式*/",
                     "QSplitter::handle:vertical":"/*垂直手柄样式*/",
                     "QSplitter::handle:pressed":"手柄按下样式"
                     },
        "QTabWidget":{"QTabWidget":
                        '''
                        /*
                        标签窗口
                        好用的属性设置
                        documentMode 文档模式
                        tabsCloseable 标签按钮上出现关闭标志
                        movable 标签可移动
                        */
                        ''',
                      "QTabWidget::pane":"/*标签下面框架的样式*/",
                      "QTabBar::tab":"/*标签样式*/",
                      "QTabWidget::tab-bar":"/*标签栏样式(设置颜色无效)*/",
                      "QTabBar::tab:hover":"/*鼠标放在标签上时的样式*/",
                      "QTabBar::tab:selected":"/*标签被选择时的样式*/",
                      "QTabBar::tab:!selected":"/*标签没有被选择时的样式*/",
                      "QTabBar::close-button":"/*关闭按钮的样式(需要将tabsCloseable设置为真才生效)*/",
                      "QTabBar::close-button:hover":"/*鼠标放在关闭按钮上时的样式(需要将tabsCloseable设置为真才生效)*/"
                      },
        "QTableView":{"QTableView":"/*表格视图*/",
                      "QTableView QTableCornerButton::section":"/*角落部件样式*/"
                      },
        "QTreeView":{"QTreeView":"/*树视图*/",
                     "QTreeView::item":"/**/",
                     "QTreeView::item:hover":"/**/",
                     "QTreeView::item:selected":"/**/",
                     "QTreeView::item:selected:active":"/**/",
                     "QTreeView::item:selected:!active":"/**/",
                     "QTreeView::branch":"/*分支样式*/"},
        "QToolBar":{"QToolBar":"/*工具栏*/",
                    "QToolBar::handle":"/*手柄样式,建议设置image属性*/",
                    "QToolBox::tab":"/*标签样式*/",
                    "QToolBox::tab:selected ":"/*标签被选择时的样式*/",
                    },
        "QMainWindow":{"QMainWindow":'''
                    /*这个是主窗口(不是控件)*/
                    ''',
                       "QMainWindow::separator":"/*分隔符样式*/",
                       "QMainWindow::separator:hover":"/*鼠标放在分隔符上时的样式*/"
                       },
        "QFrame": {"QFrame": '''
                    框架
                    支持这个选择器的控件有如下:
                    QListView
                    QListWidget
                    QTreeView
                    QTreeWidget
                    QTableView
                    QTreeWidget
                    QColumnView
                    QUndoView
                    QScrollArea
                    QToolBar
                    QStackedWidget
                    QMdiArea
                    QTextEdit
                    QTextBrowser
                    QGraphicsView
                    QLCDNumber
                    '''},
        "QStatusBar":{"QStatusBar":
                    '''
                    /*
                    状态栏
                    一般只有QMainWindow才有
                    */
                    ''',
                    "QStatusBar::item":"每一项的样式"},
        "QHeaderView":{"QHeaderView":'''
                    /*头部视图(这个不是控件),是选择器,
                    支持这个选择器的控件有如下:
                    QTreeView
                    QTreeWidget
                    QTableView
                    QTreeWidget
                    */
                    ''',
                    "QHeaderView::section":"/*行和列头部的样式*/",
                    "QHeaderView::section:checked":"/*行和列头部按下时的样式*/",
                    "QHeaderView::down-arrow":"/*排序指示器的样式(需要将sortingEnabled设置为真才生效)*/",
                    "QHeaderView::up-arrow":"/*排序指示器的样式(需要将sortingEnabled设置为真才生效)*/"},
        "QAbstractScrollArea": {"QAbstractScrollArea": '''
                    /*滑块组件*/
                    (这个不是控件),是选择器,
                    支持这个选择器的控件有如下:
                    QListView
                    QListWidget
                    QTreeView
                    QTreeWidget
                    QTableView
                    QTreeWidget
                    QColumnView
                    QUndoView
                    '''
                    },
        "QSizeGrip":{"QSizeGrip":
                    '''
                    /*
                    (这个不是控件),是选择器
                    它的作用是改变窗口拉伸提示,需要属性设置image
                    mainwindow默认在状态栏右下角
                    */
                    '''
                     },
        "QToolTip":{"QToolTip":
                    '''
                        (这个不是控件),是选择器
                        提示类,需要给xx.setToolTip()设置之后才生效
                    '''},
    }
    # 属性
    attrs = {
        "background":{
            "background-color":"/*背景颜色*/",
            "background-image":'''
            /*
            背景图片
            background-image:url(:/xxx/xxx.png);
            */''',
            "background-repeat":'''
            /*
            背景重复
            background-repeat:值;
            值:
                repeat 不重复
                repeat-x 只在x轴重复
                repeat-y 只在y轴重复
            */''',
            "background-position":'''
            /*
            背景对齐方式
            语法： 
                background-position : length  length 
                background-position : position  position 
            取值： 
                length:百分数 | 由浮点数字和单位标识符组成的长度值
                position:top | center | bottom | left | center | right 
            Eg:
                background-position:50% 50%;
                background-position:center bottom;
            */''',
            "background-attachment":
            '''
            /*
                背景图像是相对于视口滚动还是固定(默认滚动)
                background-attachment:fixed;   固定
            */''',
        },
        "border":{"border-radius":"/*边框圆角*/",
                  "border-style":"/*边框样式*/",
                  "border-width":"/*边框宽度*/",
                  "border-color":"/*边框颜色*/",
                  "border-top-left-radius":"/*左上角圆角*/",
                  "border-top-right-radius":"/*右上角圆角*/",
                  "border-bottom-left-radius":"/*左下角圆角*/",
                  "border-bottom-right-radius":"/*右下角圆角*/",
                  "border-image":"/*图片*/",
                  "border-image-source":"/*图片路径*/",
                  "border-image-repeat":"/*重复方式*/",
                  "border-image-slice":"/*切片*/",
                  "border-image-width":"/*宽度*/",
                  "border-image-outset":"/*边距*/",},
        'color':{"text-decoration":"/*文本装饰*/",
                 "text-align":"/*文本对齐方式*/",
                 "text-indent":"/*文本缩进*/",
                 "text-shadow":"/*文本阴影*/",
                 "text-transform":"/*文本转换*/",
                 "text-overflow":"/*文本溢出*/",
                 "text-decoration-color":"/*文本装饰颜色*/",
                 "text-decoration-style":"/*文本装饰样式*/",
                 "text-decoration-line":"/*文本装饰线*/",
},

    }

    @staticmethod
    def help():
        print("请在showControl()使用以下参数")
        for k in ControlLib.controls.keys():
            v = ControlLib.controls[k][k].replace("/*","")
            v = v.replace("*/","")
            # print(k,"==>",v)
            print("\033[1;34m{}\033[0m".format(k), end="")
            print(" ==> ",end="")
            print("\033[1;30m{}\033[0m".format(v))

    # 控件铺平
    @staticmethod
    def controls_list()->list:
        controls_ = list(ControlLib.controls.keys())
        attrs_ = list(ControlLib.attrs.keys())
        for v in ControlLib.controls.values():
            controls_.extend(list(v.keys()))

        for v in ControlLib.attrs.values():
            controls_.extend(list(v.keys()))

        return controls_+attrs_


def showAttrs(control,x):
    pass

def showControl(control):
    '''
    显示该控件所有的样式操作方法
    :param control: 控件名称(选择器)
    :return:
    '''
    print("[==========<{}==========]".format(control))
    # ControlLib.controls[control]
    for ck,cv in ControlLib.controls[control].items():
        print("\033[1;34m{}\033[0m".format(ck), end="")
        print("\033[1;37m{}\033[0m".format("{"))
        if cv:
            print("\033[1;32m{}\033[0m".format(cv))
        print("\033[1;37m{}\033[0m".format("}"))
    print("[=========={}>==========]".format(control))
    # return ControlLib.controls[control]
# showControl("QRadioButton")
# ControlLib.help()

def getStyleStr(control:str, pseudo_state: list = None):
    '''
    返回一个该control所有可操作样式的空字符串
    Eg:
        control=QPushButton 返回的结果
        QPushButton{
        }
        QPushButton:houver{
        }
        QPushButton:pressed{
        }
        QPushButton::menu-indicator{
        }
        ...
    如果指定的副属性,那么只会返回和副属性有关的样式 ["hover"]
    返回结果:
        QPushButton{
        }
        QPushButton:houver{
        }
    如果指只想返回与控件名称相同的属性
    EG:
        control = QPushButton
        deputyProperties = [" "]
    返回结果:
        QPushButton{
        }
    :param control: 控件名称(选择器)
    :param pseudo_state: 控件名称(选择器)的副属性(伪状态)
        例如 hover,pressed,...
    :return:
    '''
    qss = ''''''
    new_dict = ControlLib.controls[control]
    if not pseudo_state:
        for k in new_dict.keys():
            qss+=k+"{\n}\n"
    else:

        qss+=control+"{\n}\n"
        for k in new_dict.keys():
            for de in pseudo_state:
                if re.findall(de,k):
                    qss += k + "{\n}\n"
    return qss
# print(getStyleStr("QSplitter",["horizontal"]))
