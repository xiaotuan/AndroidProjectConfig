import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Memory:
    """
    内存处理类

    默认处理方法：
        修改 device/mediateksample/公版名称/ProjectConfig.mk 和 vendor/mediatek/proprietary/bootable/bootloader/preloader/custom/公版名称/公版名称.mk 文件的如下宏：
            CUSTOM_CONFIG_MAX_DRAM_SIZE = 0xc0000000
    """


    TAG = "Memory"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getMemorySize(self):
        """
        获取当前内存大小
        """
        size = ""
        originConfigPath = self.info.projectDir + "/device/mediateksample/" + self.info.publicName + "/ProjectConfig.mk"
        customConfigPath = self.info.driveDir + "/config/ProjectConfig.mk"
        if os.path.exists(customConfigPath):
            try:
                with open(customConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.strip().startswith("CUSTOM_CONFIG_MAX_DRAM_SIZE"):
                            values = line.split("=")
                            if len(values) == 2 and len(values[1].strip()) > 0:
                                size = values[1].strip()
                            break
            except:
                self.log.e(self.TAG, "getFingerprint=>error: " + traceback.format_exc())
        
        if len(size) == 0:
            with open(originConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.strip().startswith("CUSTOM_CONFIG_MAX_DRAM_SIZE"):
                        values = line.split("=")
                        if len(values) == 2 and len(values[1].strip()) > 0:
                            size = values[1].strip()
                        break
        self.log.d(self.TAG, "getMemorySize=>size: " + size)
        return size


    def setMemorySize(self, size):
        """
        设置内存大小

        Parameters:
            size - 内存大小
        """
        self.log.d(self.TAG, "setMemorySize=>size: " + size)
        result = False
        hasCustomFile = False
        hasCustomPlFile = False
        tempConfigPath = None
        tempPlConfigPath = None
        customConfigPath = self.info.driveDir + "/config/ProjectConfig.mk"
        customPlConfigPath = self.info.driveDir + "/config/" + self.info.publicName + "_pl.mk"
        
        if os.path.exists(customConfigPath):
            hasCustomFile = True
            tempConfigPath = TEMP_DIR_NAME + "/" + os.path.basename(customConfigPath)
            shutil.copy(customConfigPath, tempConfigPath)

        if os.path.exists(customPlConfigPath):
            hasCustomPlFile = True
            tempPlConfigPath = TEMP_DIR_NAME + "/" + os.path.basename(customPlConfigPath)
            shutil.copy(customPlConfigPath, tempPlConfigPath)

        try:
            content = None
            if hasCustomFile:
                with open(customConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
            with open(customConfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                if not hasCustomFile:
                    file.write("CUSTOM_CONFIG_MAX_DRAM_SIZE = " + size + "\n")
                else:
                    for line in content:
                        if line.strip().startswith("CUSTOM_CONFIG_MAX_DRAM_SIZE"):
                            file.write("CUSTOM_CONFIG_MAX_DRAM_SIZE = " + size + "\n")
                        else:
                            file.write(line)

            if hasCustomPlFile:
                with open(customPlConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
            with open(customPlConfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                if not hasCustomFile:
                    file.write("CUSTOM_CONFIG_MAX_DRAM_SIZE = " + size + "\n")
                else:
                    for line in content:
                        if line.strip().startswith("CUSTOM_CONFIG_MAX_DRAM_SIZE"):
                            file.write("CUSTOM_CONFIG_MAX_DRAM_SIZE = " + size + "\n")
                        else:
                            file.write(line)

            result = True
        except:
            self.log.e(self.TAG, "setMemorySize=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempConfigPath):
                    shutil.copy(tempConfigPath, customConfigPath)
            else:
                if os.path.exists(customConfigPath):
                    os.remove(customConfigPath)

            if hasCustomPlFile:
                if os.path.exists(tempPlConfigPath):
                    shutil.copy(tempPlConfigPath, customPlConfigPath)
            else:
                if os.path.exists(customPlConfigPath):
                    os.remove(customPlConfigPath)
            
        if tempConfigPath is not None and os.path.exists(tempConfigPath):
            os.remove(tempConfigPath)

        if tempPlConfigPath is not None and os.path.exists(tempPlConfigPath):
            os.remove(tempPlConfigPath)

        return result