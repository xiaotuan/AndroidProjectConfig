

from tkinter import *
from tkinter.ttk import *

from sample.samplecontroller import SampleController


class SampleView:
    """
    送样视图类
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
        self.controller = SampleController(self, self.info, self.log)
        self.sampleStatus = IntVar()
        self.sampleStatus.set(0)


    def initViews(self):
        """
        初始化子视图
        """
        self.sampleLabel = Label(self.frame, text="送样状态：")
        self.sampleOffRadioButton = Radiobutton(self.frame, text="关闭", value=0, variable=self.sampleStatus)
        self.sampleOnRadioButton = Radiobutton(self.frame, text="打开", value=1, variable=self.sampleStatus)
        self.sampleStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.sampleSetButton = Button(self.frame, text="设置", command=self.controller.setSampleStatus)

        # 送样软件的型号和名称
        self.sampleNameLabel = Label(self.frame, text="送样名称：")
        self.sampleNameEntry = Entry(self.frame)
        self.sampleNameStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.sampleNameSetButton = Button(self.frame, text="设置", command=self.controller.setSampleName)

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