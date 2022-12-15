
from tkinter import *
from tkinter.ttk import *

from tee.teecontroller import TeeController


class TeeView:
    """
    tee 选项卡视图
    """

    TAG = "TeeView"


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
        self.controller = TeeController(self, self.info, self.log)
        self.status = IntVar()
        self.status.set(0)


    def initViews(self):
        """
        初始化视图
        """

        # Tee 状态
        self.teeLabel = Label(self.frame, text="TEE 状态：")
        self.teeOffRadioButton = Radiobutton(self.frame, text="关闭", value=0, variable=self.status)
        self.teeOnRadioButton = Radiobutton(self.frame, text="打开", value=1, variable=self.status)
        self.teeStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.teeButton = Button(self.frame, text="设置", command=self.controller.setTeeStatus)

        # array.c
        self.arrayLabel = Label(self.frame, text="array.c 文件路径：")
        self.arrayEntry = Entry(self.frame)
        self.arraySelectButton = Button(self.frame, text="选择", command=self.controller.selectArrayFile)
        self.arrayStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.arraySetButton = Button(self.frame, text="设置", command=self.controller.setArrayFile)

        # cert.dat
        self.certLabel = Label(self.frame, text="cert.dat 文件路径：")
        self.certEntry = Entry(self.frame)
        self.certSelectButton = Button(self.frame, text="选择", command=self.controller.selectCertFile)
        self.certStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.certSetButton = Button(self.frame, text="设置", command=self.controller.setCertFile)

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
