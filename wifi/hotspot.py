import os
import time
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Hotspot:
    """
    WiFi 热点名称管理类

    默认修改方法：
        修改 packages/modules/Wifi/service/java/com/android/server/wifi/WifiApConfigStore.java 文件中 getDefaultApConfiguration() 方法的如下代码：
            configBuilder.setSsid(mContext.getResources().getString(
                R.string.wifi_tether_configure_ssid_default) + "_" + getRandomIntForDefaultSsid());
    """

    TAG = "Hotspot"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getHotspotName(self):
        """
        获取当前 WiFi 热点名称
        """
        name = ""
        customWacsPath = self.info.customDir + "/alps/packages/modules/Wifi/service/java/com/android/server/wifi/WifiApConfigStore.java"
        if os.path.exists(customWacsPath):
            with open(customWacsPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                isInFunction = False
                count = 0
                for line in content:
                    if isInFunction and line.strip().startswith('configBuilder.setSsid(') and line.strip().endswith(';'):
                        self.log.d(self.TAG, "getHotspotName=>line: " + line)
                        name = line.strip()[len('configBuilder.setSsid("'):len(line)]
                        name = name[0:(len(name) - len('");'))]
                        break
                    elif line.strip().startswith('private SoftApConfiguration getDefaultApConfiguration() {'):
                        isInFunction = True
                        count += 1
                    elif isInFunction and line.strip().endswith("{"):
                        count += 1
                    elif isInFunction and count > 0 and line.strip().endswith("}"):
                        count -= 1
                        if count == 0:
                            isInFunction = False
        self.log.d(self.TAG, "getHotspotName=>name: " + name)
        return name


    def setHotspotName(self, name):
        """
        设置 WiFi 热点名称

        Parameter:
            name - WiFi 热点名称
        """
        result = False
        hasCustomFile = False
        tempWacsPath = None
        originWacsPath = self.info.projectDir + "/packages/modules/Wifi/service/java/com/android/server/wifi/WifiApConfigStore.java"
        customWacsPath = self.info.customDir + "/alps/packages/modules/Wifi/service/java/com/android/server/wifi/WifiApConfigStore.java"
        if os.path.exists(customWacsPath):
            hasCustomFile = True
            tempWacsPath = TEMP_DIR_NAME + "/" + os.path.basename(customWacsPath)
            shutil.copy(customWacsPath, tempWacsPath)
        else:
            if not os.path.exists(os.path.dirname(customWacsPath)):
                os.makedirs(os.path.dirname(customWacsPath))
            shutil.copy(originWacsPath, customWacsPath)

        try:
            content = None
            with open(customWacsPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customWacsPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    isInFunction = False
                    count = 0
                    for line in content:
                        if isInFunction:
                            if hasCustomFile:
                                if line.strip().startswith('configBuilder.setSsid("') and line.strip().endswith('");'):
                                    file.write('        configBuilder.setSsid("' + name + '");\n')
                                else:
                                    file.write(line)
                            else:
                                if line.strip().startswith('configBuilder.setSsid(mContext.getResources().getString('):
                                    file.write('        // configBuilder.setSsid(mContext.getResources().getString(\n')
                                elif line.strip().startswith('R.string.wifi_tether_configure_ssid_default) + "_" + getRandomIntForDefaultSsid());'):
                                    file.write('        //         R.string.wifi_tether_configure_ssid_default) + "_" + getRandomIntForDefaultSsid());\n')
                                    file.write('        configBuilder.setSsid("' + name + '");\n')
                                else:
                                    file.write(line)
                        else:
                            file.write(line)
                            if line.strip().startswith('private SoftApConfiguration getDefaultApConfiguration() {'):
                                isInFunction = True
                                count += 1
                            elif isInFunction and line.strip().endswith("{"):
                                count += 1
                            elif count > 0 and line.strip().endswith("}"):
                                count -= 1
                                if count == 0:
                                    isInFunction = False

                result = True
        except:
            self.log.e(self.TAG, "setVersionDefault=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempWacsPath):
                    shutil.copy(tempWacsPath, customWacsPath)
            else:
                if os.path.exists(customWacsPath):
                    os.remove(customWacsPath)
            
        if tempWacsPath is not None and os.path.exists(tempWacsPath):
            os.remove(tempWacsPath)

        return result