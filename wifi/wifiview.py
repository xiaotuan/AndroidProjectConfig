from tkinter import *
from tkinter.ttk import *

from wifi.wificontroller import WifiController


class WifiView:
    """
    WiFi 视图类
    """


    TAG = "WifiView"


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
        self.controller = WifiController(self, self.info, self.log)
        self.wifiStatus = IntVar()
        self.wifiStatus.set(0)


    def initViews(self):
        """
        初始化子视图
        """
        self.wifiLabel = Label(self.frame, text="WiFi 状态：")
        self.wifiOffRadioButton = Radiobutton(self.frame, text="关闭", value=0, variable=self.wifiStatus)
        self.wifiOnRadioButton = Radiobutton(self.frame, text="打开", value=1, variable=self.wifiStatus)
        self.wifiStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.wifiSetButton = Button(self.frame, text="设置", command=self.controller.setWifiStatus)

        # WiFi 热点名称
        self.hotspotLabel = Label(self.frame, text="WiFi 热点名称：")
        self.hotspotEntry = Entry(self.frame)
        self.hotspotStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.hotspotSetButton = Button(self.frame, text="设置", command=self.controller.setHotspotName)

        # WiFi 投射名称
        self.dartLabel = Label(self.frame, text="WiFi 投射直连名称：")
        self.dartEntry = Entry(self.frame)
        self.dartStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.dartSetButton = Button(self.frame, text="设置", command=self.controller.setDartName)

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
        self.controller.updateViewsInfo()