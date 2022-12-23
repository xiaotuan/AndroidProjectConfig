import os
import time
import traceback
import shutil

from constant import TEMP_DIR_NAME

class BtStatus:
    """
    设置蓝牙状态类

    默认处理方法：
        修改 vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml 文件中的如下代码：
            <bool name="def_bluetooth_on">false</bool>
    """


    TAG = "BtStatus"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getBluetoothStatus(self):
        """
        获取蓝牙状态
        """
        result = False
        originDefaultPath = self.info.projectDir + "/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"
        customDefaultPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"
        if os.path.exists(customDefaultPath):
            with open(customDefaultPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.strip().startswith('<bool name="def_bluetooth_on">'):
                        value = line.strip()[len('<bool name="def_bluetooth_on">'):len(line)].strip()
                        value = value[0:(len(value) - len('</bool>'))]
                        self.log.d(self.TAG, "getBluetoothStatus=>value: " + value)
                        result = value == "true"
        else:
            with open(originDefaultPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.strip().startswith('<bool name="def_bluetooth_on">'):
                        value = line.strip()[len('<bool name="def_bluetooth_on">'):len(line)].strip()
                        value = value[0:(len(value) - len('</bool>'))]
                        self.log.d(self.TAG, "getBluetoothStatus=>value: " + value)
                        result = value == "true"
        self.log.d(self.TAG, "getBluetoothStatus=>status: " + str(result))
        return result


    def setBluetoothStatus(self, enabled):
        """
        设置蓝牙状态

        Parameters:
            enabled - True - 蓝牙默认打开，False - 蓝牙默认关闭
        """
        self.log.d(self.TAG, "setBluetoothStatus=>enabled: " + str(enabled))
        result = False
        hasCustomFile = False
        tempDefaultPath = None
        originDefaultPath = self.info.projectDir + "/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"
        customDefaultPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"
        if os.path.exists(customDefaultPath):
            hasCustomFile = True
            tempDefaultPath = TEMP_DIR_NAME + "/" + os.path.basename(customDefaultPath)
            shutil.copy(customDefaultPath, tempDefaultPath)
        else:
            if not os.path.exists(os.path.dirname(customDefaultPath)):
                os.makedirs(os.path.dirname(customDefaultPath))
            shutil.copy(originDefaultPath, customDefaultPath)

        try:
            content = None
            with open(customDefaultPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customDefaultPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if line.strip().startswith('<bool name="def_bluetooth_on">'):
                            if enabled:
                                file.write('    <bool name="def_bluetooth_on">true</bool>\n')
                            else:
                                file.write('    <bool name="def_bluetooth_on">false</bool>\n')
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setBluetoothStatus=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempDefaultPath):
                    shutil.copy(tempDefaultPath, customDefaultPath)
            else:
                if os.path.exists(customDefaultPath):
                    os.remove(customDefaultPath)
            
        if tempDefaultPath is not None and os.path.exists(tempDefaultPath):
            os.remove(tempDefaultPath)

        return result