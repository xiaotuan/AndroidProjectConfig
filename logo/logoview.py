from tkinter import *
from tkinter.ttk import *

from logo.logocontroller import LogoController


class LogoView:
    """
    Logo 选项卡视图
    """

    TAG = "LogoView"


    def __init__(self, frame, info, log):
        self.log = log
        self.frame = frame
        self.info = info

        self.initValues()
        self.initViews()


    def initValues(self):
        """
        初始化变量
        """
        self.controller = LogoController(self, self.info, self.log)


    def initViews(self):
        """
        初始子控件
        """
        self.logoLabel = Label(self.frame, text="Logo 图片路径：")
        self.logoEntry = Entry(self.frame)
        self.logoSelectButton = Button(self.frame, text="选择", command=self.controller.selectLogo)
        self.logoShowButton = Button(self.frame, text="查看", command=self.controller.showLogo)
        self.logoStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.logoSetButton = Button(self.frame, text="设置", command=self.controller.setLogo)
        

    def onSizeChanged(self, width, height):
        """
        窗口尺寸改变处理方法
        """
        self.log.d(self.TAG, "onSizeChanged=>width: " + str(width) + ", height: " + str(height))
        self.controller.layoutViews(width, height)


    def updateViewInfo(self):
        """
        更新控件信息
        """
        self.log.d(self.TAG, "updateViewInfo()...")
        self.controller.updateViewsInfo()