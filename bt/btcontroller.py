from tkinter import DISABLED, NORMAL
from bt.bluetooth import Bluetooth
from constant import *


class BtController:
    """
    蓝牙视图控制类
    """


    TAG = "BtController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.bluetooth = Bluetooth(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.btStateLabel.config(text="        ")
        self.view.btNameStateLabel.config(text="        ")
        if not self.info.isEmpty():
            self.view.btSetButton.configure(state=NORMAL)
            self.view.btNameSetButton.configure(state=NORMAL)
            self.view.allSetButton.configure(state=NORMAL)
            
            if self.bluetooth.getBluetoothStatus():
                self.view.btStatus.set(1)
            else:
                self.view.btStatus.set(0)
            self.view.btNameEntry.delete(0, 'end')
            self.view.btNameEntry.insert(0, self.bluetooth.getBluetoothName())
        else:
            self.view.btSetButton.configure(state=DISABLED)
            self.view.btNameSetButton.configure(state=DISABLED)
            self.view.allSetButton.configure(state=DISABLED)


    def setBluetoothStatus(self):
        """
        设置蓝牙状态
        """
        enabled = False
        if self.view.btStatus.get() == 1:
            enabled = True
        if self.bluetooth.setBluetoothStatus(enabled):
            self.view.btStateLabel.config(text="PASS")
            self.view.btStateLabel.config(foreground='green')
        else:
            self.view.btStateLabel.config(text="FAIL")
            self.view.btStateLabel.config(foreground='red')


    def setBluetoothName(self):
        """
        设置蓝牙名称
        """
        name = self.view.btNameEntry.get().strip()
        if len(name) > 0:
            if self.bluetooth.setBluetoothName(name):
                self.view.btNameStateLabel.config(text="PASS")
                self.view.btNameStateLabel.config(foreground='green')
            else:
                self.view.btNameStateLabel.config(text="FAIL")
                self.view.btNameStateLabel.config(foreground='red')


    def setAll(self):
        """
        设置全部
        """
        self.setBluetoothStatus()
        self.setBluetoothName()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width

        # 蓝牙状态
        self.view.btSetButton.place(x=max_width- (CHILD_MARGIN_RIGHT + self.view.btSetButton.winfo_width()), y=y)

        self.view.btStateLabel.place(x=max_width - (CHILD_MARGIN_RIGHT + self.view.btSetButton.winfo_width() 
            + self.view.btStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT),
            y=y + (self.view.btSetButton.winfo_height()
            - self.view.btOffRadioButton.winfo_height()) / 2)

        self.view.btLabel.place(x=x, y=y + (self.view.btSetButton.winfo_height() 
            - self.view.btLabel.winfo_height()) / 2)

        x += self.view.btLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.btOffRadioButton.place(x=x, y=y + (self.view.btSetButton.winfo_height()
            - self.view.btOffRadioButton.winfo_height()) / 2)

        x += self.view.btOffRadioButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.btOnRadioButton.place(x=x, y=y + (self.view.btSetButton.winfo_height()
            - self.view.btOnRadioButton.winfo_height()) / 2)

        # 蓝牙名称
        x = CONTAINER_MARGIN_LEFT
        y += self.view.btNameSetButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.btNameLabel.place(x=x, y=y)

        y += self.view.btNameLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.btNameSetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.btNameSetButton.place(x=last_x, y=y)

        last_x -= self.view.btNameStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.btNameStateLabel.place(x=last_x, y=y + (self.view.btNameSetButton.winfo_height() - self.view.btNameStateLabel.winfo_height()) / 2)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.btNameEntry.place(x=x, y=y + (self.view.btNameSetButton.winfo_height() - self.view.btNameEntry.winfo_height()) / 2,
            width=last_x - x)


        # 按钮
        y += self.view.btNameSetButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.allSetButton.place(x=(max_width - self.view.allSetButton.winfo_width()) / 2, y=y)