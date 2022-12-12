import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Device:
    """
    设备处理类

    修改 device/mediateksample/公版名称/vnd_公版名称.mk 文件中的如下代码
        PRODUCT_SYSTEM_DEVICE := tb8788p1_64_bsp_k419
    """

    TAG = "Device"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getDevice(self):
        """
        获取设备
        """
        device = ""
        hasCustomFile = False
        vndPath = "device/mediateksample/" + self.info.publicName + "/vnd_" + self.info.publicName + ".mk"
        originVndPath = self.info.projectDir + "/" + vndPath
        customVndPath = self.info.customDir + "/alps/" + vndPath
        content = None
        if os.path.exists(customVndPath):
            hasCustomFile = True
            with open(customVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        else:
            with open(originVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        
        if content is not None:
            prefix = "PRODUCT_SYSTEM_DEVICE :="
            if not hasCustomFile:
                prefix = "PRODUCT_DEVICE :="
            for line in content:
                if line.startswith(prefix):
                    device = line[len(prefix):len(line)].strip()
                    break;
        return device


    def setDevice(self, device):
        """
        设置设备
        """
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        vndPath = "device/mediateksample/" + self.info.publicName + "/vnd_" + self.info.publicName + ".mk"
        originVndPath = self.info.projectDir + "/" + vndPath
        customVndPath = self.info.customDir + "/alps/" + vndPath
        if os.path.exists(customVndPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customVndPath)
            shutil.copy(customVndPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customVndPath)):
                os.makedirs(os.path.dirname(customVndPath))
            shutil.copy(originVndPath, customVndPath)

        try:
            content = None
            with open(customVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                hasMacro = False
                for line in content:
                    if line.startswith("PRODUCT_SYSTEM_DEVICE :="):
                        hasMacro = True
                        break;
                with open(customVndPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if hasMacro:
                            if line.startswith("PRODUCT_SYSTEM_DEVICE :="):
                                file.write("PRODUCT_SYSTEM_DEVICE := " + device + "\n")
                            else:
                                file.write(line)
                        else:
                            if line.startswith("PRODUCT_BRAND :="):
                                file.write(line)
                                file.write("\n")
                                file.write("PRODUCT_SYSTEM_DEVICE := " + device + "\n")
                            else:
                                file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setDevice=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customVndPath)
            else:
                if os.path.exists(customVndPath):
                    os.remove(customVndPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result