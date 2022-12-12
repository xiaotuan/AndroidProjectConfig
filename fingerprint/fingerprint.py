
import os
import traceback
import shutil

from constant import TEMP_DIR_NAME

class Fingerprint:
    """
    Fingerprint 管理类

    默认修改方法：
        FULL 编译修改方法：
            修改 device/mediatek/system/common/BoardConfig.mk 文件中的如下内容：
                BUILD_NUMBER_WEIBU := $(shell date +%s)

        分割编译修改方法：
            1. 修改 device/mediatek/system/common/BoardConfig.mk 文件中的如下内容：
                BUILD_NUMBER_WEIBU := $(shell date +%s)
            2. 修改 device/mediatek/vendor/common/BoardConfig.mk 文件中的如下内容：
                BUILD_NUMBER_WEIBU := $(shell date +%s)
    """

    TAG = "Version"
    BOARDCONFIG_PATH = "device/mediatek/system/common/BoardConfig.mk"

    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getFingerprint(self):
        """
        获取当前工程的 Fingerprint
        """
        fp = ""
        customBoardConfigPath = self.info.customDir + "/alps/" + self.BOARDCONFIG_PATH
        if os.path.exists(customBoardConfigPath):
            try:
                with open(customBoardConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("WEIBU_BUILD_NUMBER :="):
                            fp = line[len("WEIBU_BUILD_NUMBER :="):len(line) - 1].strip()
                            break
            except:
                self.log.e(self.TAG, "getFingerprint=>error: " + traceback.format_exc())
        else:
            self.log.i(self.TAG, "getFingerprint=>" + customBoardConfigPath + " file not found!")
        return fp


    def setFingerprint(self, fingerprint):
        """
        设置 Fingerprint

        Parameters:
            fingerprint - 要设置的 fingerprint 值
        """
        return self.setFingerprintDefault(fingerprint)


    def setFingerprintDefault(self, fingerprint):
        """
        默认设置 Fingerprint  方法

        Parameters:
            fingerprint - 要设置的 fingerprint 值
        """
        self.log.d(self.TAG, "setFingerprintDefault=>fingerprint: " + fingerprint)
        result = False
        hasCustomFile = False
        tempBoardConfigPath = None
        originBoardConfigPath = self.info.projectDir + "/" + self.BOARDCONFIG_PATH
        customBoardConfigPath = self.info.customDir + "/alps/" + self.BOARDCONFIG_PATH
        if os.path.exists(customBoardConfigPath):
            hasCustomFile = True
            tempBoardConfigPath = TEMP_DIR_NAME + "/" + os.path.basename(customBoardConfigPath)
            shutil.copy(customBoardConfigPath, tempBoardConfigPath)
        else:
            if not os.path.exists(os.path.dirname(customBoardConfigPath)):
                os.makedirs(os.path.dirname(customBoardConfigPath))
            shutil.copy(originBoardConfigPath, customBoardConfigPath)

        try:
            content = None
            with open(customBoardConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customBoardConfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    
                    for line in content:
                        if line.startswith("WEIBU_BUILD_NUMBER :="):
                            file.write("WEIBU_BUILD_NUMBER := " + fingerprint + "\n")
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setFingerprintDefault=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBoardConfigPath):
                    shutil.copy(tempBoardConfigPath, customBoardConfigPath)
            else:
                if os.path.exists(customBoardConfigPath):
                    os.remove(customBoardConfigPath)
            
        if tempBoardConfigPath is not None and os.path.exists(tempBoardConfigPath):
            os.remove(tempBoardConfigPath)

        return result