from tkinter import DISABLED, NORMAL
from sample.sample import Sample
from constant import *



class SampleController:
    """
    送样视图控制类
    """

    TAG = "SampleController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.sample = Sample(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.sampleStateLabel.config(text="        ")
        self.view.sampleNameStateLabel.config(text="        ")
        if not self.info.isEmpty():
            self.view.sampleSetButton.configure(state=NORMAL)
            self.view.sampleNameSetButton.configure(state=NORMAL)
            self.view.allSetButton.configure(state=NORMAL)
            
            if self.sample.getStatus():
                self.view.sampleStatus.set(1)
            else:
                self.view.sampleStatus.set(0)
            self.view.sampleNameEntry.delete(0, 'end')
            self.view.sampleNameEntry.insert(0, self.sample.getName())
        else:
            self.view.sampleSetButton.configure(state=DISABLED)
            self.view.sampleNameSetButton.configure(state=DISABLED)
            self.view.allSetButton.configure(state=DISABLED)


    def setSampleStatus(self):
        """
        设置送样状态
        """
        enabled = False
        if self.view.sampleStatus.get() == 1:
            enabled = True
        if self.sample.setStatus(enabled):
            self.view.sampleStateLabel.config(text="PASS")
            self.view.sampleStateLabel.config(foreground='green')
        else:
            self.view.sampleStateLabel.config(text="FAIL")
            self.view.sampleStateLabel.config(foreground='red')


    def setSampleName(self):
        """
        设置送样名称
        """
        name = self.view.sampleNameEntry.get().strip()
        if len(name) > 0:
            if self.sample.setName(name):
                self.view.sampleNameStateLabel.config(text="PASS")
                self.view.sampleNameStateLabel.config(foreground='green')
            else:
                self.view.sampleNameStateLabel.config(text="FAIL")
                self.view.sampleNameStateLabel.config(foreground='red')


    def setAll(self):
        """
        设置全部
        """
        self.setSampleStatus()
        self.setSampleName()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width

        # 送样状态
        self.view.sampleSetButton.place(x=max_width- (CHILD_MARGIN_RIGHT + self.view.sampleSetButton.winfo_width()), y=y)

        self.view.sampleStateLabel.place(x=max_width - (CHILD_MARGIN_RIGHT + self.view.sampleSetButton.winfo_width() 
            + self.view.sampleStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT),
            y=y + (self.view.sampleSetButton.winfo_height()
            - self.view.sampleOffRadioButton.winfo_height()) / 2)

        self.view.sampleLabel.place(x=x, y=y + (self.view.sampleSetButton.winfo_height() 
            - self.view.sampleLabel.winfo_height()) / 2)

        x += self.view.sampleLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.sampleOffRadioButton.place(x=x, y=y + (self.view.sampleSetButton.winfo_height()
            - self.view.sampleOffRadioButton.winfo_height()) / 2)

        x += self.view.sampleOffRadioButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.sampleOnRadioButton.place(x=x, y=y + (self.view.sampleSetButton.winfo_height()
            - self.view.sampleOnRadioButton.winfo_height()) / 2)

        # 送样名称
        x = CONTAINER_MARGIN_LEFT
        y += self.view.sampleNameSetButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.sampleNameLabel.place(x=x, y=y)

        y += self.view.sampleNameLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.sampleNameSetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.sampleNameSetButton.place(x=last_x, y=y)

        last_x -= self.view.sampleNameStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.sampleNameStateLabel.place(x=last_x, y=y + (self.view.sampleNameSetButton.winfo_height() - self.view.sampleNameStateLabel.winfo_height()) / 2)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.sampleNameEntry.place(x=x, y=y + (self.view.sampleNameSetButton.winfo_height() - self.view.sampleNameEntry.winfo_height()) / 2,
            width=last_x - x)


        # 按钮
        y += self.view.sampleNameSetButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.allSetButton.place(x=(max_width - self.view.allSetButton.winfo_width()) / 2, y=y)