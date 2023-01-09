import os
import traceback
import shutil

from constant import TEMP_DIR_NAME

class SampleStatus:
    """
    处理送样状态
    """

    TAG = "SampleStatus"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getStatus(self):
        """
        获取送样状态
        """
        result = False
        drivePath = self.info.driveDir + "/config/ProjectConfig.mk"
        customPath = self.info.customDir + "/config/ProjectConfig.mk"
        if os.path.exists(customPath):
            with open(customPath, newline='\n', mode='r', encoding='utf-8') as file:
                contents = file.readlines()
                for line in contents:
                    if line.strip().startswith("WEIBU_PRODUCT_SAMPLE_GMS"):
                        values = line.strip().split("=")
                        if len(values) == 2 and values[1].strip() == 'yes':
                            result = True
                            break
        if not result and os.path.exists(drivePath):
            with open(drivePath, newline='\n', mode='r', encoding='utf-8') as file:
                contents = file.readlines()
                for line in contents:
                    if line.strip().startswith("WEIBU_PRODUCT_SAMPLE_GMS"):
                        values = line.strip().split("=")
                        if len(values) == 2 and values[1].strip() == 'yes':
                            result = True
                            break
        self.log.d(self.TAG, "getStatus=>result: " + str(result))
        return result;


    def setStatus(self, enabled):
        """
        设置送样状态

        Parameters:
            enabled - True 打开送样宏，False 关闭送样宏
        """
        result = False
        hasCustomFile = False
        tempPath = None
        customPath = self.info.customDir + "/config/ProjectConfig.mk"
        if os.path.exists(customPath):
            hasCustomFile = True
            tempPath = TEMP_DIR_NAME + "/" + os.path.basename(customPath)
            shutil.copy(customPath, tempPath)
        else:
            if not os.path.exists(os.path.dirname(customPath)):
                os.makedirs(os.path.dirname(customPath))

        try:
            content = None
            if hasCustomFile:
                with open(customPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
            with open(customPath, mode='w+', newline='\n', encoding='utf-8') as file:
                if hasCustomFile:
                    for line in content:
                        if line.strip().startswith("WEIBU_PRODUCT_SAMPLE_GMS"):
                            file.write('WEIBU_PRODUCT_SAMPLE_GMS = yes\n')
                        else:
                            file.write(line)
                else:
                    file.write('WEIBU_PRODUCT_SAMPLE_GMS = yes\n')
            result = True
        except:
            self.log.e(self.TAG, "setStatus=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempPath):
                    shutil.copy(tempPath, customPath)
            else:
                if os.path.exists(customPath):
                    os.remove(customPath)
            
        if tempPath is not None and os.path.exists(tempPath):
            os.remove(tempPath)

        return result