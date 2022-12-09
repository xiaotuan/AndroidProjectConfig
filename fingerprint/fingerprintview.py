from tkinter import *
from tkinter.ttk import *

from fingerprint.fingerprintcontroller import FingerprintController

class FingerprintView:
    """
    Fingerprint 选项卡视图
    """

    TAG = "FingerprintView"


    def __init__(self, frame, info, log):
        self.log = log
        self.frame = frame
        self.info = info

        self.initValues()
        self.initViews()
        self.bindViewEvent()


    def initValues(self):
        """
        初始化变量
        """
        self.log.d(self.TAG, "initValues()...")
        self.controller = FingerprintController(self, self.info, self.log)


    def initViews(self):
        """
        初始化控件
        """
        self.log.d(self.TAG, "initViews()...")
        self.fingerprintLabel = Label(self.frame, text="Fingerprint: ")
        self.fingerprintEntry = Entry(self.frame)
        self.fingerprintStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.fingerprintButton = Button(self.frame, text="设置", command=self.controller.setFingerprint)
        self.fingerprintRandomButton = Button(self.frame, text="随机设置", command=self.controller.randomSetFingerprint)
 

    def bindViewEvent(self):
        """
        绑定控件事件
        """
        self.log.d(self.TAG, "bindViewEvent()...")
        self.fingerprintEntry.bind("<KeyRelease>", self.controller.fingerprintChanged)

    
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