
from wifi.wifistatus import WifiStatus
from wifi.hotspot import Hotspot
from wifi.dart import Dart

class Wifi:
    """
    WIFI 处理类
    """

    TAG = "WiFi"


    def __init__(self, info, log):
        self.log = log
        self.info = info
        self.wifiStatus = WifiStatus(self.info, self.log)
        self.hotspot = Hotspot(self.info, self.log)
        self.dart = Dart(self.info, self.log)


    def getWifiStatus(self):
        """
        获取当前 WiFi 状态
        """
        return self.wifiStatus.getWifiStatus()


    def setWifiStatus(self, enabled):
        """
        设置 WiFi 状态
        
        Parameters:
            enabled - WiFi 状态
        """
        return self.wifiStatus.setWifiStatus(enabled)


    def getHotspotName(self):
        """
        获取当前 WiFi 热点名称
        """
        return self.hotspot.getHotspotName()


    def setHotspotName(self, name):
        """
        设置 WiFi 热点名称

        Parameters:
            name - WiFi 热点名称
        """
        return self.hotspot.setHotspotName(name)


    def getDartName(self):
        """
        获取当前 WiFi 投射名称
        """
        return self.dart.getDartName()


    def setDartName(self, name):
        """
        设置 WiFi 投射名称

        Parameters:
            name - WiFi投射名称
        """
        return self.dart.setDartName(name)