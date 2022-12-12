
from system.brand import Brand
from system.device import Device
from system.mode import Mode
from system.name import Name
from system.manufacturer import Manufacturer
from system.language import Language
from system.timezone import Timezone


class System:
    """
    系统选项卡操作类
    """

    TAG = "System"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getBrand(self):
        """
        获取品牌名称
        """
        brand = Brand(self.info, self.log)
        return brand.getBrand()


    def setBrand(self, name):
        """
        设置品牌名称
        """
        self.log.d(self.TAG, "setBrand=>name: " + name)
        brand = Brand(self.info, self.log)
        return brand.setBrand(name)


    def getMode(self):
        """
        获取型号
        """
        mode = Mode(self.info, self.log)
        return mode.getMode()


    def setMode(self, name):
        """
        设置型号
        """
        self.log.d(self.TAG, "setMode=>name: " + name)
        mode = Mode(self.info, self.log)
        return mode.setMode(name)


    def getName(self):
        """
        获取设备名称
        """
        name = Name(self.info, self.log)
        return name.getName()


    def setName(self, n):
        """
        设置设备名称
        """
        self.log.d(self.TAG, "setName=>name: " + n)
        name = Name(self.info, self.log)
        return name.setName(n)

    
    def getDevice(self):
        """
        获取设备
        """
        device = Device(self.info, self.log)
        return device.getDevice()


    def setDevice(self, name):
        """
        设置设备
        """
        self.log.d(self.TAG, "setDevice=>name: " + name)
        device = Device(self.info, self.log)
        return device.setDevice(name)


    def getManufacturer(self):
        """
        获取制造商
        """
        manufacturer = Manufacturer(self.info, self.log)
        return manufacturer.getManufacturer()


    def setManufacturer(self, name):
        """
        设置制造商
        """
        self.log.d(self.TAG, "setManufacturer=>name: " + name)
        manufacturer = Manufacturer(self.info, self.log)
        return manufacturer.setManufacturer(name)


    def getLanguage(self):
        """
        获取语言
        """
        language = Language(self.info, self.log)
        return language.getLanguage()


    def setLanguage(self, name):
        """
        设置语言
        """
        self.log.d(self.TAG, "setLanguage=>name: " + name)
        language = Language(self.info, self.log)
        return language.setLanguage(name)


    def getTimezone(self):
        """
        获取时区
        """
        timezone = Timezone(self.info, self.log)
        return timezone.getTimezone()


    def setTimezone(self, name):
        """
        设置时区
        """
        self.log.d(self.TAG, "setTimezone=>name: " + name)
        timezone = Timezone(self.info, self.log)
        return timezone.setTimezone(name)
