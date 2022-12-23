from tkinter import *
from tkinter.ttk import *

from bt.bluetooth import Bluetooth
from bt.btcontroller import BtController


class BtView:
    """
    蓝牙视图类
    """


    TAG = "BtView"


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
        self.controller = BtController(self, self.info, self.log)
        self.btStatus = IntVar()
        self.btStatus.set(0)


    def initViews(self):
        """
        初始化子视图
        """
        self.btLabel = Label(self.frame, text="蓝牙状态：")
        self.btOffRadioButton = Radiobutton(self.frame, text="关闭", value=0, variable=self.btStatus)
        self.btOnRadioButton = Radiobutton(self.frame, text="打开", value=1, variable=self.btStatus)
        self.btStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.btSetButton = Button(self.frame, text="设置", command=self.controller.setBluetoothStatus)

        # WiFi 热点名称
        self.btNameLabel = Label(self.frame, text="蓝牙名称：")
        self.btNameEntry = Entry(self.frame)
        self.btNameStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.btNameSetButton = Button(self.frame, text="设置", command=self.controller.setBluetoothName)

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