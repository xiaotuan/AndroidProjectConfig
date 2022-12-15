
from tkinter import DISABLED, NORMAL
from constant import CHILD_MARGIN_LEFT, CHILD_MARGIN_RIGHT, CHILD_MARGIN_TOP, CONTAINER_MARGIN_LEFT, CONTAINER_MARGIN_RIGHT, CONTAINER_MARGIN_TOP
from system.system import System


class SystemController:
    """
    系统选项卡视图控制器
    """

    TAG = "SystemController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.system = System(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.brandStateLabel.config(text="        ")
        self.view.modeStateLabel.config(text="        ")
        self.view.nameStateLabel.config(text="        ")
        self.view.deviceStateLabel.config(text="        ")
        self.view.manufacturerStateLabel.config(text="        ")
        self.view.languageStateLabel.config(text="        ")
        self.view.timezoneStateLabel.config(text="        ")

        if self.info.isEmpty():
            self.view.brandEntry.delete(0, 'end')
            self.view.brandEntry.insert(0, self.system.getBrand())

            self.view.modeEntry.delete(0, 'end')
            self.view.modeEntry.insert(0, self.system.getMode())

            self.view.nameEntry.delete(0, 'end')
            self.view.nameEntry.insert(0, self.system.getName())

            self.view.deviceEntry.delete(0, 'end')
            self.view.deviceEntry.insert(0, self.system.getDevice())

            self.view.manufacturerEntry.delete(0, 'end')
            self.view.manufacturerEntry.insert(0, self.system.getManufacturer())

            self.view.languageEntry.delete(0, 'end')
            self.view.languageEntry.insert(0, self.system.getLanguage())

            self.view.timezoneEntry.delete(0, 'end')
            self.view.timezoneEntry.insert(0, self.system.getTimezone())

        if not self.info.isEmpty():
            self.view.brandButton.configure(state=NORMAL)
            self.view.modeButton.configure(state=NORMAL)
            self.view.nameButton.configure(state=NORMAL)
            self.view.deviceButton.configure(state=NORMAL)
            self.view.manufacturerButton.configure(state=NORMAL)
            self.view.languageButton.configure(state=NORMAL)
            self.view.timezoneButton.configure(state=NORMAL)
            self.view.allSetButton.configure(state=NORMAL)
        else:
            self.view.brandButton.configure(state=DISABLED)
            self.view.modeButton.configure(state=DISABLED)
            self.view.nameButton.configure(state=DISABLED)
            self.view.deviceButton.configure(state=DISABLED)
            self.view.manufacturerButton.configure(state=DISABLED)
            self.view.languageButton.configure(state=DISABLED)
            self.view.timezoneButton.configure(state=DISABLED)
            self.view.allSetButton.configure(state=DISABLED)


    def setBrand(self):
        """
        设置品牌名称
        """
        self.log.d(self.TAG, "setBrand()...")
        brand = self.view.brandEntry.get().strip()
        if len(brand) > 0:
            if self.system.setBrand(brand):
                self.view.brandStateLabel.config(text="PASS")
                self.view.brandStateLabel.config(foreground='green')
            else:
                self.view.brandStateLabel.config(text="FAIL")
                self.view.brandStateLabel.config(foreground='red')


    def setMode(self):
        """
        设置型号
        """
        self.log.d(self.TAG, "setMode()...")
        mode = self.view.modeEntry.get().strip()
        if len(mode) > 0:
            if self.system.setMode(mode):
                self.view.modeStateLabel.config(text="PASS")
                self.view.modeStateLabel.config(foreground='green')
            else:
                self.view.modeStateLabel.config(text="FAIL")
                self.view.modeStateLabel.config(foreground='red')


    def setName(self):
        """
        设置名称
        """
        self.log.d(self.TAG, "setName()...")
        name = self.view.nameEntry.get().strip()
        if len(name) > 0:
            if self.system.setName(name):
                self.view.nameStateLabel.config(text="PASS")
                self.view.nameStateLabel.config(foreground='green')
            else:
                self.view.nameStateLabel.config(text="FAIL")
                self.view.nameStateLabel.config(foreground='red')


    def setDevice(self):
        """
        设置设备
        """
        device = self.view.deviceEntry.get().strip()
        if len(device) > 0:
            if self.system.setDevice(device):
                self.view.deviceStateLabel.config(text="PASS")
                self.view.deviceStateLabel.config(foreground='green')
            else:
                self.view.deviceStateLabel.config(text="FAIL")
                self.view.deviceStateLabel.config(foreground='red')


    def setManufacturer(self):
        """
        设置制造商
        """
        self.log.d(self.TAG, "setManufacturer()...")
        manufacturer = self.view.manufacturerEntry.get().strip()
        if len(manufacturer) > 0:
            if self.system.setManufacturer(manufacturer):
                self.view.manufacturerStateLabel.config(text="PASS")
                self.view.manufacturerStateLabel.config(foreground='green')
            else:
                self.view.manufacturerStateLabel.config(text="FAIL")
                self.view.manufacturerStateLabel.config(foreground='red')


    def setLanguage(self):
        """
        设置语言
        """
        self.log.d(self.TAG, "setLanguage()...")
        language = self.view.languageEntry.get().strip()
        if len(language) > 0:
            if self.system.setLanguage(language):
                self.view.languageStateLabel.config(text="PASS")
                self.view.languageStateLabel.config(foreground='green')
            else:
                self.view.languageStateLabel.config(text="FAIL")
                self.view.languageStateLabel.config(foreground='red')


    def setTimezone(self):
        """
        设置时区
        """
        self.log.d(self.TAG, "setTimezone()...")
        timezone = self.view.timezoneEntry.get().strip()
        if len(timezone) > 0:
            if self.system.setTimezone(timezone):
                self.view.timezoneStateLabel.config(text="PASS")
                self.view.timezoneStateLabel.config(foreground='green')
            else:
                self.view.timezoneStateLabel.config(text="FAIL")
                self.view.timezoneStateLabel.config(foreground='red')

    
    def setAll(self):
        """
        全部设置
        """
        self.log.d(self.TAG, "setAll()...")
        self.setBrand()
        self.setMode()
        self.setManufacturer()
        self.setName()
        self.setDevice()
        self.setLanguage()
        self.setTimezone()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        self.log.d(self.TAG, "layoutViews=>width: " + str(width) + ", height: " + str(height))
        top = 0
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width
        label_width = 50

        # 品牌
        last_x = max_width - self.view.brandButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.brandButton.place(x=last_x, y=y)

        button_height = self.view.brandButton.winfo_height()
        last_x -= self.view.brandStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.brandStateLabel.place(x=last_x, y=y + (button_height - self.view.brandStateLabel.winfo_height()) / 2);
        
        self.view.brandLabel.place(x=x, y=y + (button_height - self.view.brandLabel.winfo_height()), width=label_width)

        x += self.view.brandLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.brandEntry.place(x=x, y=y + (button_height - self.view.brandEntry.winfo_height()), width=entry_width)

        # 型号
        x = CONTAINER_MARGIN_LEFT
        y += self.view.brandButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.modeButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.modeButton.place(x=last_x, y=y)

        button_height = self.view.modeButton.winfo_height()
        last_x -= self.view.modeStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.modeStateLabel.place(x=last_x, y=y + (button_height - self.view.modeStateLabel.winfo_height()) / 2);
        
        self.view.modeLabel.place(x=x, y=y + (button_height - self.view.modeLabel.winfo_height()), width=label_width)

        x += self.view.modeLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.modeEntry.place(x=x, y=y + (button_height - self.view.modeEntry.winfo_height()), width=entry_width)

        # 名称
        x = CONTAINER_MARGIN_LEFT
        y += self.view.nameButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.nameButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.nameButton.place(x=last_x, y=y)

        button_height = self.view.nameButton.winfo_height()
        last_x -= self.view.nameStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.nameStateLabel.place(x=last_x, y=y + (button_height - self.view.nameStateLabel.winfo_height()) / 2);
        
        self.view.nameLabel.place(x=x, y=y + (button_height - self.view.nameLabel.winfo_height()), width=label_width)

        x += self.view.nameLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.nameEntry.place(x=x, y=y + (button_height - self.view.nameEntry.winfo_height()), width=entry_width)

        # 设备
        # 名称
        x = CONTAINER_MARGIN_LEFT
        y += self.view.nameButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.deviceButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.deviceButton.place(x=last_x, y=y)

        button_height = self.view.deviceButton.winfo_height()
        last_x -= self.view.deviceStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.deviceStateLabel.place(x=last_x, y=y + (button_height - self.view.deviceStateLabel.winfo_height()) / 2);
        
        self.view.deviceLabel.place(x=x, y=y + (button_height - self.view.deviceLabel.winfo_height()), width=label_width)

        x += self.view.deviceLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.deviceEntry.place(x=x, y=y + (button_height - self.view.deviceEntry.winfo_height()), width=entry_width)

        # 制造商
        x = CONTAINER_MARGIN_LEFT
        y += self.view.deviceButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.manufacturerButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.manufacturerButton.place(x=last_x, y=y)

        button_height = self.view.manufacturerButton.winfo_height()
        last_x -= self.view.manufacturerStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.manufacturerStateLabel.place(x=last_x, y=y + (button_height - self.view.manufacturerStateLabel.winfo_height()) / 2);
        
        self.view.manufacturerLabel.place(x=x, y=y + (button_height - self.view.manufacturerLabel.winfo_height()), width=label_width)

        x += self.view.manufacturerLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.manufacturerEntry.place(x=x, y=y + (button_height - self.view.manufacturerEntry.winfo_height()), width=entry_width)

        # 语言
        x = CONTAINER_MARGIN_LEFT
        y += self.view.languageButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.languageButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.languageButton.place(x=last_x, y=y)

        button_height = self.view.languageButton.winfo_height()
        last_x -= self.view.languageStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.languageStateLabel.place(x=last_x, y=y + (button_height - self.view.languageStateLabel.winfo_height()) / 2);
        
        self.view.languageLabel.place(x=x, y=y + (button_height - self.view.languageLabel.winfo_height()), width=label_width)

        x += self.view.languageLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.languageEntry.place(x=x, y=y + (button_height - self.view.languageEntry.winfo_height()), width=entry_width)

        # 时区
        x = CONTAINER_MARGIN_LEFT
        y += self.view.timezoneButton.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - self.view.timezoneButton.winfo_width() - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT
        self.view.timezoneButton.place(x=last_x, y=y)

        button_height = self.view.timezoneButton.winfo_height()
        last_x -= self.view.timezoneStateLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        self.view.timezoneStateLabel.place(x=last_x, y=y + (button_height - self.view.timezoneStateLabel.winfo_height()) / 2);
        
        self.view.timezoneLabel.place(x=x, y=y + (button_height - self.view.timezoneLabel.winfo_height()), width=label_width)

        x += self.view.timezoneLabel.winfo_width() + CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT
        entry_width = last_x - CHILD_MARGIN_RIGHT - CHILD_MARGIN_LEFT - x
        self.view.timezoneEntry.place(x=x, y=y + (button_height - self.view.timezoneEntry.winfo_height()), width=entry_width)

        # 按钮
        y += self.view.timezoneButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.allSetButton.place(x=(max_width - self.view.allSetButton.winfo_width()) / 2, y=y)