from tkinter import *
from tkinter.ttk import *

from memory.memorycontroller import MemoryController


class MemoryView:
    """
    内存视图
    """

    TAG = "MemoryView"


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
        self.controller = MemoryController(self, self.info, self.log)


    def initViews(self):
        """
        初始化子试图
        """
        self.memoryLabel = Label(self.frame, text="内存大小（例如：0xC0000000）: ")
        self.memoryEntry = Entry(self.frame)
        self.memoryStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.memoryButton = Button(self.frame, text="设置", command=self.controller.setMemorySize)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.controller.updateViewsInfo()


    def onSizeChanged(self, width, height):
        """
        布局子控件
        """
        self.controller.layoutViews(width, height)