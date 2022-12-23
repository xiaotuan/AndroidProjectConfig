

from tkinter import DISABLED, NORMAL
from constant import *
from wifi.wifi import Wifi


class WifiController:
    """
    Wifi 视图控制类
    """

    TAG = "WifiController"


    def __init__(self, view, info, log):
        self.log = log
        self.info = info
        self.view = view
        self.wifi = Wifi(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.wifiStateLabel.config(text="        ")
        self.view.hotspotStateLabel.config(text="        ")
        self.view.dartStateLabel.config(text="        ")
        if not self.info.isEmpty():
            self.view.wifiSetButton.configure(state=NORMAL)
            self.view.hotspotSetButton.configure(state=NORMAL)
            self.view.dartSetButton.configure(state=NORMAL)
            self.view.allSetButton.configure(state=NORMAL)
            
            if self.wifi.getWifiStatus():
                self.view.wifiStatus.set(1)
            else:
                self.view.wifiStatus.set(0)
            self.view.hotspotEntry.delete(0, 'end')
            self.view.hotspotEntry.insert(0, self.wifi.getHotspotName())
            self.view.dartEntry.delete(0, 'end')
            self.view.dartEntry.insert(0, self.wifi.getDartName())
        else:
            self.view.wifiSetButton.configure(state=DISABLED)
            self.view.hotspotSetButton.configure(state=DISABLED)
            self.view.dartSetButton.configure(state=DISABLED)
            self.view.allSetButton.configure(state=DISABLED)


    def setWifiStatus(self):
        """
        设置 wifi 状态
        """
        enabled = False
        if self.view.wifiStatus.get() == 1:
            enabled = True
        if self.wifi.setWifiStatus(enabled):
            self.view.wifiStateLabel.config(text="PASS")
            self.view.wifiStateLabel.config(foreground='green')
        else:
            self.view.wifiStateLabel.config(text="FAIL")
            self.view.wifiStateLabel.config(foreground='red')


    def setHotspotName(self):
        """
        设置 wifi 热点名称
        """
        name = self.view.hotspotEntry.get().strip()
        if len(name) > 0:
            if self.wifi.setHotspotName(name):
                self.view.hotspotStateLabel.config(text="PASS")
                self.view.hotspotStateLabel.config(foreground='green')
            else:
                self.view.hotspotStateLabel.config(text="FAIL")
                self.view.hotspotStateLabel.config(foreground='red')


    def setDartName(self):
        """
        设置 WiFi 投射名称
        """
        name = self.view.dartEntry.get().strip()
        if len(name) > 0:
            if self.wifi.setDartName(name):
                self.view.dartStateLabel.config(text="PASS")
                self.view.dartStateLabel.config(foreground='green')
            else:
                self.view.dartStateLabel.config(text="FAIL")
                self.view.dartStateLabel.config(foreground='red')


    def setAll(self):
        """
        设置全部
        """
        self.setWifiStatus()
        self.setHotspotName()
        self.setDartName()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width

        # WiFi 状态
        self.view.wifiSetButton.place(x=max_width- (CHILD_MARGIN_RIGHT + self.view.wifiSetButton.winfo_width()), y=y)

        self.view.wifiStateLabel.place(x=max_width - (CHILD_MARGIN_RIGHT + self.view.wifiSetButton.winfo_width() 
            + self.view.wifiStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT),
            y=y + (self.view.wifiSetButton.winfo_height()
            - self.view.wifiOffRadioButton.winfo_height()) / 2)

        self.view.wifiLabel.place(x=x, y=y + (self.view.wifiSetButton.winfo_height() 
            - self.view.wifiLabel.winfo_height()) / 2)

        x += self.view.wifiLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.wifiOffRadioButton.place(x=x, y=y + (self.view.wifiSetButton.winfo_height()
            - self.view.wifiOffRadioButton.winfo_height()) / 2)

        x += self.view.wifiOffRadioButton.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.wifiOnRadioButton.place(x=x, y=y + (self.view.wifiSetButton.winfo_height()
            - self.view.wifiOnRadioButton.winfo_height()) / 2)

        # WiFi 热点
        x = CONTAINER_MARGIN_LEFT
        y += self.view.wifiSetButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.hotspotLabel.place(x=x, y=y)

        y += self.view.hotspotLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.hotspotSetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.hotspotSetButton.place(x=last_x, y=y)

        last_x -= self.view.hotspotStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.hotspotStateLabel.place(x=last_x, y=y + (self.view.hotspotSetButton.winfo_height() - self.view.hotspotStateLabel.winfo_height()) / 2)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.hotspotEntry.place(x=x, y=y + (self.view.hotspotSetButton.winfo_height() - self.view.hotspotEntry.winfo_height()) / 2,
            width=last_x - x)

        # WiFi 投射
        x = CONTAINER_MARGIN_LEFT
        y += self.view.hotspotSetButton.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.dartLabel.place(x=x, y=y)

        y += self.view.dartLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (self.view.dartSetButton.winfo_width() + CHILD_MARGIN_RIGHT)
        self.view.dartSetButton.place(x=last_x, y=y)

        last_x -= self.view.dartStateLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.dartStateLabel.place(x=last_x, y=y + (self.view.dartSetButton.winfo_height() - self.view.dartStateLabel.winfo_height()) / 2)

        last_x -=  CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.dartEntry.place(x=x, y=y + (self.view.dartSetButton.winfo_height() - self.view.dartEntry.winfo_height()) / 2,
            width=last_x - x)


        # 按钮
        y += self.view.dartSetButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.allSetButton.place(x=(max_width - self.view.allSetButton.winfo_width()) / 2, y=y)