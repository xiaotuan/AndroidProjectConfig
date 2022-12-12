import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Name:
    """
    设备名称处理类

    修改 device/mediateksample/公版名称/vnd_公版名称.mk 文件中的如下代码
        PRODUCT_SYSTEM_NAME := tb8788p1_64_bsp_k419
    """

    TAG = "Name"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getName(self):
        """
        获取设备名称
        """
        name = ""
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
            prefix = "PRODUCT_SYSTEM_NAME :="
            if not hasCustomFile:
                prefix = "PRODUCT_NAME :="
            for line in content:
                if line.startswith(prefix):
                    name = line[len(prefix):len(line)].strip()
                    break;
        return name


    def setName(self, name):
        """
        设置设备名称
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
                    if line.startswith("PRODUCT_SYSTEM_NAME :="):
                        hasMacro = True
                        break;
                with open(customVndPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if hasMacro:
                            if line.startswith("PRODUCT_SYSTEM_NAME :="):
                                file.write("PRODUCT_SYSTEM_NAME := " + name + "\n")
                            else:
                                file.write(line)
                        else:
                            if line.startswith("PRODUCT_BRAND :="):
                                file.write(line)
                                file.write("\n")
                                file.write("PRODUCT_SYSTEM_NAME := " + name + "\n")
                            else:
                                file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setName=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customVndPath)
            else:
                if os.path.exists(customVndPath):
                    os.remove(customVndPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result