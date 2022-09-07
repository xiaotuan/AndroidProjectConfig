from cgitb import text
from hashlib import new
from operator import ne
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox
import traceback
import os
import shutil

from system_property_config import SystemPropertyConfig

class SystemProperty():
    """
    系统属性设置界面
    """

    def __init__(self, frame, config, log):
        # 日志标签
        self.tag = "SystemProperty"
        # Tee 设置界面框架
        self.frame = frame
        # 工程配置对象
        self.projectConfig = config
        # TEE 配置对象
        self.config = SystemPropertyConfig(log)
        # 客制化目录路径, 用于判断当前项目是否已经改变
        self.customPath = ""
        # 日志记录类
        self.log = log

        # 初始化 UI 控件
        self.initUI()
        # 绑定 UI 事件
        self.bindUIEvent()
        # 更新 UI 信息
        self.updateUIInfo()


    def initUI(self):
        """
        初始化 UI 事件
        """
        # 品牌
        self.brandLabel = Label(self.frame, text="品牌：")
        self.brandEntry = Entry(self.frame)
        self.brandStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setBrandButton = Button(self.frame, text="设置", command=self.setBrand)

        # 型号
        self.modelLabel = Label(self.frame, text="型号：")
        self.modelEntry = Entry(self.frame)
        self.modelStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setModelButton = Button(self.frame, text="设置", command=self.setModel)

        # 设备
        self.deviceLabel = Label(self.frame, text="设备：")
        self.deviceEntry = Entry(self.frame)
        self.deviceStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setDeviceButton = Button(self.frame, text="设置", command=self.setDevice)

        # 制造商
        self.manufacturerLabel = Label(self.frame, text="制造商：")
        self.manufacturerEntry = Entry(self.frame)
        self.manufacturerStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setManufacturerButton = Button(self.frame, text="设置", command=self.setManufacturer)

        # 名称
        self.nameLabel = Label(self.frame, text="名称：")
        self.nameEntry = Entry(self.frame)
        self.nameStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setNameButton = Button(self.frame, text="设置", command=self.setName)

        # 语言
        self.languageLabel = Label(self.frame, text="语言：")
        self.languageEntry = Entry(self.frame)
        self.languageStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setLanguageButton = Button(self.frame, text="设置", command=self.setLanguage)

        # 时区
        self.timeZoneLabel = Label(self.frame, text="时区：")
        self.timeZoneEntry = Entry(self.frame)
        self.timeZoneStateLabel = Label(self.frame, text="", foreground='green', anchor='center')
        self.setTimeZoneButton = Button(self.frame, text="设置", command=self.setTimeZone)

        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.brandEntry.bind("<KeyRelease>", self.brandChanged)
        self.modelEntry.bind("<KeyRelease>", self.modelChanged)
        self.deviceEntry.bind("<KeyRelease>", self.deviceChanged)
        self.manufacturerEntry.bind("<KeyRelease>", self.manufacturerChanged)
        self.nameEntry.bind("<KeyRelease>", self.nameChanged)
        self.languageEntry.bind("<KeyRelease>", self.languageChanged)
        self.timeZoneEntry.bind("<KeyRelease>", self.timeZoneChanged)
        

    def layout(self, width, height):
        """
        布局 UI 控件
        """
        self.log.d(self.tag, "[layout] width: " + str(width) + ", height: " + str(height))
        x = 10
        y = 15
        stateLabelWidth = 36

        # 品牌
        hx = width - x - self.setBrandButton.winfo_width()
        self.setBrandButton.place(x=hx, y=y)
        hx -= x + self.brandStateLabel.winfo_width()
        self.brandStateLabel.place(x=hx, y=y + (self.setBrandButton.winfo_height() - self.brandStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.brandLabel.place(x=x, y=y + (self.setBrandButton.winfo_height() - self.brandLabel.winfo_height()) / 2)
        self.brandEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setBrandButton.winfo_height() - self.brandEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 型号
        y += self.setBrandButton.winfo_height() + 10
        hx = width - x - self.setModelButton.winfo_width()
        self.setModelButton.place(x=hx, y=y)
        hx -= x + self.modelStateLabel.winfo_width()
        self.modelStateLabel.place(x=hx, y=y + (self.setModelButton.winfo_height() - self.modelStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.modelLabel.place(x=x, y=y + (self.setModelButton.winfo_height() - self.modelLabel.winfo_height()) / 2)
        self.modelEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setModelButton.winfo_height() - self.modelEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 设备
        y += self.setModelButton.winfo_height() + 10
        hx = width - x - self.setDeviceButton.winfo_width()
        self.setDeviceButton.place(x=hx, y=y)
        hx -= x + self.deviceStateLabel.winfo_width()
        self.deviceStateLabel.place(x=hx, y=y + (self.setDeviceButton.winfo_height() - self.deviceStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.deviceLabel.place(x=x, y=y + (self.setDeviceButton.winfo_height() - self.deviceLabel.winfo_height()) / 2)
        self.deviceEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setDeviceButton.winfo_height() - self.deviceEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 制造商
        y += self.setDeviceButton.winfo_height() + 10
        hx = width - x - self.setManufacturerButton.winfo_width()
        self.setManufacturerButton.place(x=hx, y=y)
        hx -= x + self.manufacturerStateLabel.winfo_width()
        self.manufacturerStateLabel.place(x=hx, y=y + (self.setManufacturerButton.winfo_height() - self.manufacturerStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.manufacturerLabel.place(x=x, y=y + (self.setManufacturerButton.winfo_height() - self.manufacturerLabel.winfo_height()) / 2)
        self.manufacturerEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setManufacturerButton.winfo_height() - self.manufacturerEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 名称
        y += self.setManufacturerButton.winfo_height() + 10
        hx = width - x - self.setNameButton.winfo_width()
        self.setNameButton.place(x=hx, y=y)
        hx -= x + self.nameStateLabel.winfo_width()
        self.nameStateLabel.place(x=hx, y=y + (self.setNameButton.winfo_height() - self.nameStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.nameLabel.place(x=x, y=y + (self.setNameButton.winfo_height() - self.nameLabel.winfo_height()) / 2)
        self.nameEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setNameButton.winfo_height() - self.nameEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 语言
        y += self.setNameButton.winfo_height() + 10
        hx = width - x - self.setLanguageButton.winfo_width()
        self.setLanguageButton.place(x=hx, y=y)
        hx -= x + self.languageStateLabel.winfo_width()
        self.languageStateLabel.place(x=hx, y=y + (self.setLanguageButton.winfo_height() - self.languageStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.languageLabel.place(x=x, y=y + (self.setLanguageButton.winfo_height() - self.languageLabel.winfo_height()) / 2)
        self.languageEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setLanguageButton.winfo_height() - self.languageEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 时区
        y += self.setLanguageButton.winfo_height() + 10
        hx = width - x - self.setTimeZoneButton.winfo_width()
        self.setTimeZoneButton.place(x=hx, y=y)
        hx -= x + self.timeZoneStateLabel.winfo_width()
        self.timeZoneStateLabel.place(x=hx, y=y + (self.setTimeZoneButton.winfo_height() - self.timeZoneStateLabel.winfo_height()) / 2, width=stateLabelWidth)
        self.timeZoneLabel.place(x=x, y=y + (self.setTimeZoneButton.winfo_height() - self.timeZoneLabel.winfo_height()) / 2)
        self.timeZoneEntry.place(x=x * 2 + self.manufacturerStateLabel.winfo_width() + x,
            y=y + (self.setTimeZoneButton.winfo_height() - self.timeZoneEntry.winfo_height()) / 2,
            width=hx - (self.manufacturerStateLabel.winfo_width() + 4 * x))

        # 按钮
        y += self.setTimeZoneButton.winfo_height() + 25
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)

    
    def updateUIInfo(self):
        """
        更新 UI 信息
        """
        self.log.d(self.tag, "[updateUIInfo] customPath: " + self.projectConfig.customPath + ", old: " + self.customPath)
        if self.projectConfig.customPath != self.customPath:
            self.config.brand = self.getBrand()
            self.config.model = self.getModel()
            self.config.device = self.getDevice()
            self.config.manufacturer = self.getManufacturer()
            self.config.name = self.getName()
            self.config.language = self.getLanguage()
            self.config.timeZone = self.getTimeZone()
            self.customPath = self.projectConfig.customPath
        self.brandEntry.delete(0, 'end')
        self.brandEntry.insert(0, self.config.brand)
        self.modelEntry.delete(0, 'end')
        self.modelEntry.insert(0, self.config.model)
        self.deviceEntry.delete(0, 'end')
        self.deviceEntry.insert(0, self.config.device)
        self.manufacturerEntry.delete(0, 'end')
        self.manufacturerEntry.insert(0, self.config.manufacturer)
        self.nameEntry.delete(0, 'end')
        self.nameEntry.insert(0, self.config.name)
        self.languageEntry.delete(0, 'end')
        self.languageEntry.insert(0, self.config.language)
        self.timeZoneEntry.delete(0, 'end')
        self.timeZoneEntry.insert(0, self.config.timeZone)


    def getBrand(self):
        """
        获取品牌
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Brand()
            else:
                self.log.w(self.tag, "[getBrand] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getBrand] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Brand(self):
        """
        获取 MediaTek Android 12 的品牌
        """
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        brand = "alps"
        if os.path.exists(customFile):
            with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("PRODUCT_BRAND"):
                        values = line.split(":=")
                        if len(values) == 2:
                            brand = values[1].strip()
                        break
        return brand


    def getModel(self):
        """
        获取型号
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Model()
            else:
                self.log.w(self.tag, "[getModel] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getModel] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Model(self):
        """
        获取 Mediatek Android 12 的型号
        """
        # WEIBU_PRODUCT_SAMPLE_GMS
        model = 'weibu'
        isSampleGmsOpened = self.isSampleGmsOpened()
        customSystemPropFile = self.projectConfig.customPath + "/config/system.prop"
        kernelSystemPropFile = self.projectConfig.driveCustomPath + "/config/system.prop"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"

        self.log.d(self.tag, "[getModel] WEIBU_PRODUCT_SAMPLE_GMS = " + str(isSampleGmsOpened))
        if isSampleGmsOpened:
            if os.path.exists(customSystemPropFile):
                with open(customSystemPropFile, mode='r', newline='\n', encoding='utf8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("persist.sys.sample.device.name"):
                            values = line.split('=')
                            if len(values) == 2:
                                model = values[1].strip()
                            break
            elif os.path.exists(kernelSystemPropFile):
                with open(kernelSystemPropFile, mode='r', newline='\n', encoding='utf8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("persist.sys.sample.device.name"):
                            values = line.split('=')
                            if len(values) == 2:
                                model = values[1].strip()
                            break
        else:
            if os.path.exists(customFile):
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("PRODUCT_MODEL"):
                            values = line.split(':=')
                            if len(values) == 2:
                                model = values[1].strip()
                            break
        
        return model

    
    def isSampleGmsOpened(self):
        """
        是否打开了 WEIBU_PRODUCT_SAMPLE_GMS 宏
        """
        isSampleGmsOpened = False
        customProjectConfigFile = self.projectConfig.customPath + "/config/ProjectConfig.mk"
        kernelProjectConfigFile = self.projectConfig.driveCustomPath + "/config/ProjectConfig.mk"

        if os.path.exists(customProjectConfigFile):
            with open(customProjectConfigFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("WEIBU_PRODUCT_SAMPLE_GMS"):
                        values = line.split('=')
                        if len(values) == 2:
                            if 'yes' == values[1].strip():
                                isSampleGmsOpened = True
                        break
        elif os.path.exists(kernelProjectConfigFile):
            with open(kernelProjectConfigFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("WEIBU_PRODUCT_SAMPLE_GMS"):
                        values = line.split('=')
                        if len(values) == 2:
                            if 'yes' == values[1].strip():
                                isSampleGmsOpened = True
                        break
        
        return isSampleGmsOpened


    def getDevice(self):
        """
        获取设备
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Device()
            else:
                self.log.w(self.tag, "[getDevice] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getDevice] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Device(self):
        """
        获取 Mediatek Android 的设备
        """
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        device = "weibu"
        if os.path.exists(customFile):
            with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("PRODUCT_SYSTEM_DEVICE"):
                        values = line.split(":=")
                        if len(values) == 2:
                            device = values[1].strip()
                        break
        return device


    def getManufacturer(self):
        """
        获取制造商
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Manufacturer()
            else:
                self.log.w(self.tag, "[getManufacturer] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getManufacturer] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Manufacturer(self):
        """
        获取 Mediatek Android 12 的制造商
        """
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        manufacturer = "alps"
        if os.path.exists(customFile):
            with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("PRODUCT_MANUFACTURER"):
                        values = line.split(":=")
                        if len(values) == 2:
                            manufacturer = values[1].strip()
                        break
        return manufacturer


    def getName(self):
        """
        获取名称
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Name()
            else:
                self.log.w(self.tag, "[getName] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getName] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Name(self):
        """
        获取 Mediatek Android 12 的名称
        """
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        name = "alps"
        if os.path.exists(customFile):
            with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("PRODUCT_SYSTEM_NAME"):
                        values = line.split(":=")
                        if len(values) == 2:
                            name = values[1].strip()
                        break
        return name


    def getLanguage(self):
        """
        获取语言
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Language()
            else:
                self.log.w(self.tag, "[getLanguage] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getLanguage] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12Language(self):
        """
        获取 Mediatek Android 12 的语言
        """
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        language = "en_US"
        if os.path.exists(customFile):
            with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("PRODUCT_LOCALES"):
                        values = line.split(":=")
                        if len(values) == 2:
                            langs = values[1].strip()
                            languages = langs.split(" ")
                            if len(languages) > 0:
                                language = languages[0]
                        break
        return language

    
    def getTimeZone(self):
        """
        获取时区
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12TimeZone()
            else:
                self.log.w(self.tag, "[getTimeZone] Unsupport Android " + self.projectConfig.androidVersion)
                return ""
        else:
            self.log.w(self.tag, "[getTimeZone] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return ""

    
    def getMtkAndroid12TimeZone(self):
        """
        获取 Mediatek Android 12 的时区
        """
        timeZone = ""
        customSystemPropFile = self.projectConfig.customPath + "/config/system.prop"
        if os.path.exists(customSystemPropFile):
            with open(customSystemPropFile, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("persist.sys.timezone"):
                        values = line.split('=')
                        if len(values) == 2:
                            timeZone = values[1].strip()
                        break
        return timeZone


    def brandChanged(self, event):
        """
        品牌改变回调方法
        """
        self.config.brand = self.brandEntry.get()


    def modelChanged(self, event):
        """
        型号改变回调方法
        """
        self.config.model = self.modelEntry.get()

    
    def deviceChanged(self, event):
        """
        设备改变回调方法
        """
        self.config.device = self.deviceEntry.get()


    def manufacturerChanged(self, event):
        """
        制造商改变回调方法
        """
        self.config.manufacturer = self.manufacturerEntry.get()


    def nameChanged(self, event):
        """
        名称改变回调方法
        """
        self.config.name = self.nameEntry.get()


    def languageChanged(self, event):
        """
        语言改变回调方法
        """
        self.config.language = self.languageEntry.get()

    
    def timeZoneChanged(self, event):
        """
        时区改变回调方法
        """
        self.config.timeZone = self.timeZoneEntry.get()


    def updateStateView(self, view, success):
        """
        更新状态文本
        """
        if success:
            view.config(text="PASS")
            view.config(foreground='green')
        else:
            view.config(text="FAIL")
            view.config(foreground='red')


    def setBrand(self):
        """
        设置品牌
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Brand()
                self.updateStateView(self.brandStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setBrand] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setBrand] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Brand(self):
        """
        设置 Mediatek Android 12 的品牌
        """
        result = False
        filePath = None
        originContent = None
        content = None
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if not os.path.exists(os.path.dirname(customFile)):
                os.makedirs(os.path.dirname(customFile))
                if not os.path.exists(os.path.dirname(customFile)):
                    self.log.e(self.tag, "[setMtkAndroid12Brand] Create directory failed.")
                    return result
            if not os.path.exists(customFile):
                shutil.copyfile(originFile, customFile)
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
            else:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                filePath = customFile
                content = originContent
            with open(customFile, mode='w+', newline='\n', encoding='utf8') as file:
                for line in content:
                    if line.startswith("PRODUCT_BRAND"):
                        line = "PRODUCT_BRAND := " + self.config.brand + "\n"
                    file.write(line)
                result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Brand] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setModel(self):
        """
        设置型号
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Model()
                self.updateStateView(self.modelStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setModel] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setModel] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Model(self):
        """
        设置 Mediatek Android 12 的型号
        """
        result = False
        filePath = None
        originContent = None
        content = None
        isSampleGmsOpened = self.isSampleGmsOpened()
        customSystemPropFile = self.projectConfig.customPath + "/config/system.prop"
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if isSampleGmsOpened:
                if not os.path.exists(customSystemPropFile):
                    with open(customSystemPropFile, mode='w+', newline="\n", encoding='utf8') as file:
                        file.write("persist.sys.sample.device.name=" + self.config.model + "\n")
                        result = True
                else:
                    with open(customSystemPropFile, mode='r', newline="\n", encoding='utf8') as file:
                        originContent = file.readlines()
                        content = originContent
                    with open(customSystemPropFile, mode='w+', newline="\n", encoding='utf8') as file:
                        hasModel = False
                        for line in content:
                            if line.startswith("persist.sys.sample.device.name"):
                                line = "persist.sys.sample.device.name=" + self.config.model + "\n"
                                hasModel = True
                            file.write(line)
                        if not hasModel:
                            file.write("\npersist.sys.sample.device.name=" + self.config.model + "\n")
                        result = True
            else:
                if not os.path.exists(customFile):
                    if not os.path.exists(os.path.dirname(customFile)):
                        os.makedirs(os.path.dirname(customFile))
                        if not os.path.exists(os.path.dirname(customFile)):
                            self.log.e(self.tag, "[setMtkAndroid12Model] Create directory " + os.path.dirname(customFile) + " fail.")
                            return result
                    shutil.copyfile(originFile, customFile)
                    if not os.path.exists(customFile):
                        self.log.e(self.tag, "[setMtkAndroid12Model] Copy file " + originFile + " fail.")
                        return result
                    with open(customFile, mode='r', newline="\n", encoding='utf8') as file:
                        content = file.readlines()
                else:
                    with open(customFile, mode='r', newline="\n", encoding='utf8') as file:
                        originContent = file.readlines()
                        content = originContent
                    filePath = customFile
                with open(customFile, mode='w+', newline="\n", encoding='utf8') as file:
                    for line in content:
                        if line.startswith("PRODUCT_MODEL"):
                            line = "PRODUCT_MODEL := " + self.config.model + "\n"
                        file.write(line)
                    result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Model] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setDevice(self):
        """
        设置设备
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Device()
                self.updateStateView(self.deviceStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setDevice] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setDevice] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Device(self):
        """
        设置 Mediatek Android 12 的设备
        """
        result = False
        filePath = None
        originContent = None
        content = None
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if not os.path.exists(os.path.dirname(customFile)):
                os.makedirs(os.path.dirname(customFile))
                if not os.path.exists(os.path.dirname(customFile)):
                    self.log.e(self.tag, "[setMtkAndroid12Device] Create directory failed.")
                    return result
            if not os.path.exists(customFile):
                shutil.copyfile(originFile, customFile)
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
            else:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                filePath = customFile
                content = originContent
            with open(customFile, mode='w+', newline='\n', encoding='utf8') as file:
                hasDevice = False
                for line in content:
                    if line.startswith("PRODUCT_SYSTEM_DEVICE"):
                        line = "PRODUCT_SYSTEM_DEVICE := " + self.config.brand + "\n"
                        hasDevice = True
                    file.write(line)
                if not hasDevice:
                    file.write("\nPRODUCT_SYSTEM_DEVICE := " + self.config.brand + "\n")
                result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Device] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setManufacturer(self):
        """
        设置制造商
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Manufacturer()
                self.updateStateView(self.manufacturerStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setManufacturer] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setManufacturer] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Manufacturer(self):
        """
        设置 Mediatek Android 12 的制造商
        """
        result = False
        filePath = None
        originContent = None
        content = None
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if not os.path.exists(os.path.dirname(customFile)):
                os.makedirs(os.path.dirname(customFile))
                if not os.path.exists(os.path.dirname(customFile)):
                    self.log.e(self.tag, "[setMtkAndroid12Manufacturer] Create directory failed.")
                    return result
            if not os.path.exists(customFile):
                shutil.copyfile(originFile, customFile)
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
            else:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                filePath = customFile
                content = originContent
            with open(customFile, mode='w+', newline='\n', encoding='utf8') as file:
                for line in content:
                    if line.startswith("PRODUCT_MANUFACTURER"):
                        line = "PRODUCT_MANUFACTURER := " + self.config.brand + "\n"
                    file.write(line)
                result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Manufacturer] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setName(self):
        """
        设置名称
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Name()
                self.updateStateView(self.nameStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setName] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setName] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Name(self):
        """
        设置 Mediatek Android 12 的名称
        """
        result = False
        filePath = None
        originContent = None
        content = None
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if not os.path.exists(os.path.dirname(customFile)):
                os.makedirs(os.path.dirname(customFile))
                if not os.path.exists(os.path.dirname(customFile)):
                    self.log.e(self.tag, "[setMtkAndroid12Name] Create directory failed.")
                    return result
            if not os.path.exists(customFile):
                shutil.copyfile(originFile, customFile)
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
            else:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                filePath = customFile
                content = originContent
            with open(customFile, mode='w+', newline='\n', encoding='utf8') as file:
                hasDevice = False
                for line in content:
                    if line.startswith("PRODUCT_SYSTEM_NAME"):
                        line = "PRODUCT_SYSTEM_NAME := " + self.config.brand + "\n"
                        hasDevice = True
                    file.write(line)
                if not hasDevice:
                    file.write("\PRODUCT_SYSTEM_NAME := " + self.config.brand + "\n")
                result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Name] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setLanguage(self):
        """
        设置语言
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Language()
                self.updateStateView(self.languageStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setLanguage] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setLanguage] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12Language(self):
        """
        设置 Mediatek Android 12 的语言
        """
        result = False
        filePath = None
        originContent = None
        content = None
        originFile = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        customFile = self.projectConfig.customPath + "/alps/device/mediateksample/" + self.projectConfig.publicVersionName + "/vnd_" + self.projectConfig.publicVersionName + ".mk"
        try:
            if not os.path.exists(os.path.dirname(customFile)):
                os.makedirs(os.path.dirname(customFile))
                if not os.path.exists(os.path.dirname(customFile)):
                    self.log.e(self.tag, "[setMtkAndroid12Language] Create directory failed.")
                    return result
            if not os.path.exists(customFile):
                shutil.copyfile(originFile, customFile)
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
            else:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                filePath = customFile
                content = originContent
            with open(customFile, mode='w+', newline='\n', encoding='utf8') as file:
                for line in content:
                    if line.startswith("PRODUCT_LOCALES"):
                        values = line.split(":=")
                        if len(values) == 2:
                            langs = values[1].strip()
                            languages = langs.split(" ")
                            line = "PRODUCT_LOCALES := " + self.config.language + " "
                            for lang in languages:
                                if lang != self.config.language:
                                    line += lang + " "
                            line += "\n"
                    file.write(line)
                result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12Language] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result


    def setTimeZone(self):
        """
        设置时区
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12TimeZone()
                self.updateStateView(self.timeZoneStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "[setTimeZone] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setTimeZone] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12TimeZone(self):
        """
        设置 Mediatek Android 12 的时区
        """
        result = False
        filePath = None
        originContent = None
        content = None
        customSystemPropFile = self.projectConfig.customPath + "/config/system.prop"
        try:
            if not os.path.exists(customSystemPropFile):
                if not os.path.exists(os.path.dirname(customSystemPropFile)):
                    os.makedirs(os.path.dirname(customSystemPropFile))
                    if not os.path.exists(os.path.dirname(customSystemPropFile)):
                        self.log.e(self.tag, "[setMtkAndroid12TimeZone] Create directory fail.")
                        return result
                with open(customSystemPropFile, mode='w+', newline='\n', encoding='utf8') as file:
                    file.write("persist.sys.timezone=" + self.config.language + "\n")
                    result = True
            else:
                with open(customSystemPropFile, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                    content = originContent
                filePath = customSystemPropFile
                with open(customSystemPropFile, mode='w+', newline='\n', encoding='utf8') as file:
                    hasTimeZone = False
                    for line in content:
                        if line.startswith("persist.sys.timezone"):
                            line = "persist.sys.timezone=" + self.config.language + "\n"
                            hasTimeZone = True
                        file.write(line)
                    if not hasTimeZone:
                        file.write("\npersist.sys.timezone=" + self.config.language + "\n")
                    result = True
        except:
            self.log.e(self.tag, "[setMtkAndroid12TimeZone] error: " + traceback.format_exc())
            if filePath is not None and originContent is not None:
                with open(filePath, mode='w+', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
        return result

    
    def readConfig(self):
        """
        读取 tee 配置文件
        """
        if self.config.read():
            self.updateUIInfo()
            messagebox.showinfo("提示", "读取配置成功。")
        else:
            messagebox.showerror("错误", "读取配置失败。")


    def saveConfig(self):
        """
        保存 tee 配置信息
        """
        if self.config.save():
            self.updateUIInfo()
            messagebox.showinfo("提示", "保存配置成功。")
        else:
            messagebox.showerror("错误", "保存配置失败。")


    def setAll(self):
        """
        设置全部按钮点击处理方法
        """
        self.setBrand()
        self.setModel()
        self.setDevice()
        self.setManufacturer()
        self.setName()
        self.setLanguage()
        self.setTimeZone()