

from tkinter import DISABLED, NORMAL
from constant import *
from memory.memory import Memory


class MemoryController:
    """
    内存视图控制类
    """


    TAG = "MemoryController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.memory = Memory(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.memoryStateLabel.config(text="       ")
        
        if not self.info.isEmpty():
            self.view.memoryEntry.delete(0, 'end')
            self.view.memoryEntry.insert(0, self.memory.getMemorySize())
            
        if not self.info.isEmpty():
            self.view.memoryButton.configure(state=NORMAL)
        else:
            self.view.memoryButton.configure(state=DISABLED)


    def setMemorySize(self):
        """
        设置内存大小
        """
        size = self.view.memoryEntry.get().strip()
        if len(size) > 0:
            if self.memory.setMemorySize(size):
                self.view.memoryStateLabel.config(text="PASS")
                self.view.memoryStateLabel.config(foreground='green')
            else:
                self.view.memoryStateLabel.config(text="FAIL")
                self.view.memoryStateLabel.config(foreground='red')


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT)

        self.view.memoryLabel.place(x=x, y=y, width=max_width)

        y += self.view.memoryLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.memoryStateLabel.place(x=max_width - CHILD_MARGIN_RIGHT - self.view.memoryStateLabel.winfo_width(),
            y=y + (self.view.memoryEntry.winfo_height() - self.view.memoryStateLabel.winfo_height()) / 2)

        self.view.memoryEntry.place(x=x, y=y, 
            width=max_width - CHILD_MARGIN_LEFT * 2 - CHILD_MARGIN_RIGHT - self.view.memoryStateLabel.winfo_width())
            
        y += self.view.memoryButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.memoryButton.place(x=(max_width - self.view.memoryButton.winfo_width()) / 2, y=y)