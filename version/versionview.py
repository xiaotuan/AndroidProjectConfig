from tkinter import *
from tkinter.ttk import *

from version.versioncontroller import VersionController


class VersionView:
    """
    修改版本号视图
    """

    TAG = "VersionView"


    def __init__(self, frame, info, log) -> None:
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
        self.controller = VersionController(self, self.info, self.log)


    def initViews(self):
        """
        初始化控件
        """
        self.log.d(self.TAG, "initViews()...")
        self.versionLabel = Label(self.frame, text="软件版本号：(例如：ML_SO0N_M10_4G_T3.GOV.V5_`date +%Y%m%d`.`echo $TARGET_BUILD_VARIANT | tr '[a-z]' '[A-Z]'`)")
        self.versionEntry = Entry(self.frame)
        self.versionStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.versionButton = Button(self.frame, text="设置", command=self.controller.setVersion)


    def bindViewEvent(self):
        """
        绑定控件事件
        """
        self.log.d(self.TAG, "bindViewEvent()...")
        self.versionEntry.bind("<KeyRelease>", self.controller.versionChanged)

    
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