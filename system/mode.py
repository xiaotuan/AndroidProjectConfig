import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Mode:
    """
    型号处理类

    默认修改方法：
        修改 device/mediateksample/公版名称/vnd_公版名称.mk 文件中的如下代码
            PRODUCT_MODEL := P10-11
    """

    TAG = "Mode"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getMode(self):
        """
        获取型号
        """
        mode = ""
        vndPath = "device/mediateksample/" + self.info.publicName + "/vnd_" + self.info.publicName + ".mk"
        originVndPath = self.info.projectDir + "/" + vndPath
        customVndPath = self.info.customDir + "/alps/" + vndPath
        content = None
        if os.path.exists(customVndPath):
            with open(customVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        else:
            with open(originVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        
        if content is not None:
            for line in content:
                if line.startswith("PRODUCT_MODEL :="):
                    mode = line[len("PRODUCT_MODEL :="):len(line)].strip()
                    break;
        return mode


    def setMode(self, mode):
        """
        设置型号
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
                with open(customVndPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    
                    for line in content:
                        if line.startswith("PRODUCT_MODEL :="):
                            file.write("PRODUCT_MODEL := " + mode + "\n")
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setMode=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customVndPath)
            else:
                if os.path.exists(customVndPath):
                    os.remove(customVndPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result