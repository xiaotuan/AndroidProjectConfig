
from tkinter import DISABLED, NORMAL, filedialog
from constant import *
from tee.tee import Tee

class TeeController:
    """
    Tee 视图控制类
    """

    TAG = "TeeController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.tee = Tee(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.log.d(self.TAG, "updateViewsInfo()...")
        self.view.teeStateLabel.config(text="        ")
        self.view.arrayStateLabel.config(text="        ")
        self.view.certStateLabel.config(text="        ")

        if not self.info.isEmpty():
            if self.tee.isTeeOpened():
                self.view.status.set(1)
            else:
                self.view.status.set(0)
        
        if not self.info.isEmpty():
            self.view.teeButton.configure(state=NORMAL)
            self.view.arraySetButton.configure(state=NORMAL)
            self.view.certSetButton.configure(state=NORMAL)
            self.view.allSetButton.configure(state=NORMAL)
        else:
            self.view.teeButton.configure(state=DISABLED)
            self.view.arraySetButton.configure(state=DISABLED)
            self.view.certSetButton.configure(state=DISABLED)
            self.view.allSetButton.configure(state=DISABLED)


    def setTeeStatus(self):
        """
        设置 TEE 状态
        """
        self.log.d(self.TAG, "setTeeStatus()...")
        enabled = False
        if self.view.status.get() == 1:
            enabled = True
        if self.tee.setTeeStatus(enabled):
            self.view.teeStateLabel.config(text="PASS")
            self.view.teeStateLabel.config(foreground='green')
        else:
            self.view.teeStateLabel.config(text="FAIL")
            self.view.teeStateLabel.config(foreground='red')


    def selectArrayFile(self):
        """
        选择 array.c 文件
        """
        self.log.d(self.TAG, "selectArrayFile()...")
        path = filedialog.askopenfilename(filetypes=[("C files","*.c")])
        self.log.d(self.TAG, "selectArrayFile=>path: " + path)
        if path is not None and path.strip() != "":
            self.view.arrayEntry.delete(0, 'end')
            self.view.arrayEntry.insert(0, path)


    def setArrayFile(self):
        """
        设置 array.c 文件
        """
        self.log.d(self.TAG, "setArrayFile()...")
        filePath = self.view.arrayEntry.get().strip()
        if len(filePath) > 0:
            if self.tee.setArrayFile(filePath):
                self.view.arrayStateLabel.config(text="PASS")
                self.view.arrayStateLabel.config(foreground='green')
            else:
                self.view.arrayStateLabel.config(text="FAIL")
                self.view.arrayStateLabel.config(foreground='red')


    def selectCertFile(self):
        """
        选择 cert.dat 文件
        """
        self.log.d(self.TAG, "selectCertFile()...")
        path = filedialog.askopenfilename(filetypes=[("cert files","*.dat")])
        self.log.d(self.TAG, "selectCertFile=>path: " + path)
        if path is not None and path.strip() != "":
            self.view.certEntry.delete(0, 'end')
            self.view.certEntry.insert(0, path)


    def setCertFile(self):
        """
        设置 cert.dat 文件
        """
        self.log.d(self.TAG, "setCertFile()...")
        filePath = self.view.certEntry.get().strip()
        if len(filePath) > 0:
            if self.tee.setCertFile(filePath):
                self.view.certStateLabel.config(text="PASS")
                self.view.certStateLabel.config(foreground='green')
            else:
                self.view.certStateLabel.config(text="FAIL")
                self.view.certStateLabel.config(foreground='red')


    def setAll(self):
        """
        全部设置
        """
        self.setTeeStatus()
        self.setArrayFile()
        self.setCertFile()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        self.log.d(self.TAG, "layoutViews=>width: " + str(width) + ", height: " + str(height))

        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width

        # Tee 状态
        self.view.teeButton.place(x=max_width- (CHILD_MARGIN_RIGHT + self.view.teeButton.winfo_width()), y=y)

        self.view.teeStateLabel.place(x=max_width - (CHILD_MARGIN_RIGHT + self.view.teeButton.winfo_width() 
            + self.view.teeStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT),
            y=y + (self.view.teeButton.winfo_height()
            - self.view.teeOffRadioButton.winfo_height()) / 2)

        self.view.teeLabel.place(x=x, y=y + (self.view.teeButton.winfo_height() 
            - self.view.teeLabel.winfo_height()) / 2)

        x += self.view.teeLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.teeOffRadioButton.place(x=x, y=y + (self.view.teeButton.winfo_height()
            - self.view.teeOffRadioButton.winfo_height()) / 2)

        x += self.view.teeOffRadioButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.teeOnRadioButton.place(x=x, y=y + (self.view.teeButton.winfo_height()
            - self.view.teeOnRadioButton.winfo_height()) / 2)

        # array.c
        x = CONTAINER_MARGIN_LEFT
        y += self.view.teeButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.arrayLabel.place(x=x, y=y)

        y += self.view.arrayLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.arraySetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.arraySetButton.place(x=last_x, y=y)

        last_x -= self.view.arrayStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.arrayStateLabel.place(x=last_x, y=y + (self.view.arraySetButton.winfo_height() - self.view.arrayStateLabel.winfo_height()) / 2)

        last_x -= self.view.arraySelectButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.arraySelectButton.place(x=last_x, y=y)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.arrayEntry.place(x=x, y=y + (self.view.arraySetButton.winfo_height() - self.view.arrayEntry.winfo_height()) / 2,
            width=last_x - x)

        # cert.dat
        x = CONTAINER_MARGIN_LEFT
        y += self.view.arraySetButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.certLabel.place(x=x, y=y)

        y += self.view.certLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.certSetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.certSetButton.place(x=last_x, y=y)

        last_x -= self.view.certStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.certStateLabel.place(x=last_x, y=y + (self.view.certSetButton.winfo_height() - self.view.certStateLabel.winfo_height()) / 2)

        last_x -= self.view.certSelectButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.certSelectButton.place(x=last_x, y=y)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.certEntry.place(x=x, y=y + (self.view.certSetButton.winfo_height() - self.view.certEntry.winfo_height()) / 2,
            width=last_x - x)

        # 按钮
        y += self.view.certSetButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.allSetButton.place(x=(max_width - self.view.allSetButton.winfo_width()) / 2, y=y)