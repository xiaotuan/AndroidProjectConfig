import os
import traceback
import shutil

from constant import TEMP_DIR_NAME

class SampleName:
    """
    处理送样名称类
    """

    TAG = "SampleName"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getName(self):
        """
        获取送样名称
        """
        name = "weibu"
        customPath = self.info.customDir + "/alps/build/make/tools/buildinfo.sh"
        if os.path.exists(customPath):
            with open(customPath, mode='r', newline='\n', encoding='utf-8') as file:
                contents = file.readlines()
                for line in contents:
                    if line.strip().startswith('echo "persist.sys.sample.device.name='):
                        values = line.strip().split("=")
                        if len(values) == 2:
                            name = values[1][0:len(values) - 1]
                        break
        self.log.d(self.TAG, "getName=>name: " + name)
        return name;


    def setName(self, name):
        """
        设置送样名称
        """
        result = False
        hasCustomFile = False
        tempPath = None
        originPath = self.info.projectDir = "/build/make/tools/buildinfo.sh"
        customPath = self.info.customDir + "/alps/build/make/tools/buildinfo.sh"
        if os.path.exists(customPath):
            hasCustomFile = True
            tempPath = TEMP_DIR_NAME + "/" + os.path.basename(customPath)
            shutil.copy(customPath, tempPath)
        else:
            if not os.path.exists(os.path.dirname(customPath)):
                os.makedirs(os.path.dirname(customPath))
            shutil.copy(originPath, customPath)

        try:
            contents = None
            hasSet = False
            with open(customPath, mode='r', newline='\n', encoding='utf-8') as file:
                contents = file.readlines()
                for line in contents:
                    if line.strip().startswith('echo "persist.sys.sample.device.name='):
                        hasSet = True
            with open(customPath, mode='w+', newline='\n', encoding='utf-8') as file:
                if hasSet:
                    for line in contents:
                        if line.strip().startswith('echo "persist.sys.sample.device.name='):
                            file.write('echo "persist.sys.sample.device.name=' + name + '"\n')
                        else:
                            file.write(line)
                else:
                    for line in contents:
                        if line.strip() == 'echo "# end build properties"':
                            file.write('echo "persist.sys.sample.device.name=' + name + '"\n')
                            file.write(line)
                        else:
                            file.write(line)
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