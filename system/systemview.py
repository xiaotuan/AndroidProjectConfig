from tkinter import *
from tkinter.ttk import *

from system.systemcontroller import SystemController


class SystemView:
    """
    系统配置视图
    """

    TAG = "SystemView"


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
        self.log.d(self.TAG, "initValues()...")
        self.controller = SystemController(self, self.info, self.log)


    def initViews(self):
        """
        初始化子控件
        """
        self.log.d(self.TAG, "initViews()...")
        # 品牌
        self.brandLabel = Label(self.frame, text="品牌：")
        self.brandEntry = Entry(self.frame)
        self.brandStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.brandButton = Button(self.frame, text="设置", command=self.controller.setBrand)

        # 型号
        self.modeLabel = Label(self.frame, text="型号：")
        self.modeEntry = Entry(self.frame)
        self.modeStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.modeButton = Button(self.frame, text="设置", command=self.controller.setMode)

        # 名称
        self.nameLabel = Label(self.frame, text="名称：")
        self.nameEntry = Entry(self.frame)
        self.nameStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.nameButton = Button(self.frame, text="设置", command=self.controller.setName)

        # 设备
        self.deviceLabel = Label(self.frame, text="设备：")
        self.deviceEntry = Entry(self.frame)
        self.deviceStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.deviceButton = Button(self.frame, text="设置", command=self.controller.setDevice)

        # 制造商
        self.manufacturerLabel = Label(self.frame, text="制造商：")
        self.manufacturerEntry = Entry(self.frame)
        self.manufacturerStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.manufacturerButton = Button(self.frame, text="设置", command=self.controller.setManufacturer)

        # 语言
        self.languageLabel = Label(self.frame, text="语言：")
        self.languageEntry = Entry(self.frame)
        self.languageStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.languageButton = Button(self.frame, text="设置", command=self.controller.setLanguage)

        # 时区
        self.timezoneLabel = Label(self.frame, text="时区：")
        self.timezoneEntry = Entry(self.frame)
        self.timezoneStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.timezoneButton = Button(self.frame, text="设置", command=self.controller.setTimezone)

        # 按钮
        self.allSetButton = Button(self.frame, text="全部设置", command=self.controller.setAll)


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
        if not self.info.isEmpty():
            self.controller.updateViewsInfo()