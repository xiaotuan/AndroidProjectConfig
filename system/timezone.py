import os
import time
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Timezone:
    """
    时区处理类

    默认修改方法：
    在 build/make/tools/buildinfo.sh 文件中添加如下内容：
        echo "persist.sys.timezone=时区"
    """

    TAG = "Name"
    BUILDINFO_PATH = "build/make/tools/buildinfo.sh"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getTimezone(self):
        """
        获取时区
        """
        timezone = ""
        customBuildinfoPath = self.info.customDir + "/alps/" + self.BUILDINFO_PATH
        if os.path.exists(customBuildinfoPath):
            try:
                with open(customBuildinfoPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("echo \"persist.sys.timezone="):
                            timezone = line[len("echo \"persist.sys.timezone="):len(line) - 2]
                            break
            except:
                self.log.e(self.TAG, "getTimezone=>error: " + traceback.format_exc())
        else:
            self.log.i(self.TAG, "getTimezone=>" + customBuildinfoPath + " file not found!")
        return timezone


    def setTimezone(self, timezone):
        """
        设置时区
        """
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
            if not os.path.exists(os.path.dirname(customBuildinfoPath)):
                os.makedirs(os.path.dirname(customBuildinfoPath))
            shutil.copy(originBuildinfoPath, customBuildinfoPath)

        try:
            content = None
            with open(customBuildinfoPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                hasTimezone = False
                for line in content:
                    if line.startswith("echo \"persist.sys.timezone="):
                        hasTimezone = True
                        break
                with open(customBuildinfoPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if hasTimezone:
                            if line.startswith("echo \"persist.sys.timezone="):
                                file.write("echo \"persist.sys.timezone=" + timezone + "\"\n")
                            else:
                                file.write(line)
                        else:
                            if line.startswith("echo \"ro.build.flavor="):
                                file.write(line)
                                file.write("echo \"persist.sys.timezone=" + timezone + "\"\n")
                            else:
                                file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setTimezone=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customBuildinfoPath)
            else:
                if os.path.exists(customBuildinfoPath):
                    os.remove(customBuildinfoPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result