
import os
import traceback
import shutil

from constant import TEMP_DIR_NAME

class Version:
    """
    软件版本号管理类

    默认修改方法：
    修改 build/make/tools/buildinfo.sh 文件中的如下内容：
        echo "ro.build.display.id=$BUILD_DISPLAY_ID"
    """

    TAG = "Version"
    BUILDINFO_PATH = "build/make/tools/buildinfo.sh"

    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getVersion(self):
        """
        获取当前工程软件版本号
        """
        softwareVersion = ""
        customBuildinfoPath = self.info.customDir + "/alps/" + self.BUILDINFO_PATH
        if os.path.exists(customBuildinfoPath):
            try:
                with open(customBuildinfoPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("echo \"ro.build.display.id="):
                            softwareVersion = line[len("echo \"ro.build.display.id="):len(line) - 2]
                            break
            except:
                self.log.e(self.TAG, "getVersion=>error: " + traceback.format_exc())
        else:
            self.log.i(self.TAG, "getVersion=>" + customBuildinfoPath + " file not found!")
        return softwareVersion


    def setVersion(self, version):
        """
        设置软件版本号

        Parameters:
            version - 软件版本号
        """
        self.log.d(self.TAG, "setVersion=>version: " + version)
        return self.setVersionDefault(version)


    def setVersionDefault(self, version):
        """
        默认设置软件版本号方法

        Parameters:
            version - 软件版本号
        """
        self.log.d(self.TAG, "setVersionDefault=>version: " + version)
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        originBuildinfoPath = self.info.projectDir + "/" + self.BUILDINFO_PATH
        customBuildinfoPath = self.info.customDir + "/alps/" + self.BUILDINFO_PATH
        if os.path.exists(customBuildinfoPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customBuildinfoPath)
            shutil.copy(customBuildinfoPath, tempBuildinfoPath)
        else:
            os.makedirs(os.path.dirname(customBuildinfoPath))
            shutil.copy(originBuildinfoPath, customBuildinfoPath)

        try:
            content = None
            with open(customBuildinfoPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customBuildinfoPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    
                    for line in content:
                        if line.startswith("echo \"ro.build.display.id="):
                            file.write("echo \"ro.build.display.id=" + version + "\"\n")
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setVersionDefault=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customBuildinfoPath)
            else:
                if os.path.exists(customBuildinfoPath):
                    os.remove(customBuildinfoPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result