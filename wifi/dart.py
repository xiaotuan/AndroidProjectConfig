import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Dart:
    """
    WiFi 投射管理类
    
    默认修改方法：
        修改 packages/modules/Wifi/service/java/com/android/server/wifi/p2p/WifiP2pServiceImpl.java 文件中 getPersistedDeviceName() 方法的返回值
    """

    TAG = "Dart"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getDartName(self):
        """
        获取 WiFi 投射名称
        """
        name = ""
        customWpsiPath = self.info.customDir + "/alps/packages/modules/Wifi/service/java/com/android/server/wifi/p2p/WifiP2pServiceImpl.java"
        if os.path.exists(customWpsiPath):
            with open(customWpsiPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                isInFunction = False
                count = 0
                for line in content:
                    if isInFunction and line.strip().startswith('return "') and line.strip().endswith(';'):
                        self.log.d(self.TAG, "getDartName=>line: " + line)
                        name = line.strip()[len('return "'):len(line)]
                        name = name[0:(len(name) - len('";'))]
                    elif line.strip().startswith('private String getPersistedDeviceName() {'):
                        isInFunction = True
                        count += 1
                    elif isInFunction and line.strip().endswith("{"):
                        count += 1
                    elif isInFunction and line.strip().endswith("}"):
                        count -= 1
                        if count == 0:
                            isInFunction = False
        self.log.d(self.TAG, "getDartName=>name: " + name)
        return name


    def setDartName(self, name):
        """
        设置 WiFi 投射名称

        Parameters:
            name - WiFi 投射名称
        """
        self.log.d(self.TAG, "setDartName=>name: " + name)
        result = False
        hasCustomFile = False
        tempWpsiPath = None
        originWpsiPath = self.info.projectDir + "/packages/modules/Wifi/service/java/com/android/server/wifi/p2p/WifiP2pServiceImpl.java"
        customWpsiPath = self.info.customDir + "/alps/packages/modules/Wifi/service/java/com/android/server/wifi/p2p/WifiP2pServiceImpl.java"
        if os.path.exists(customWpsiPath):
            hasCustomFile = True
            tempWpsiPath = TEMP_DIR_NAME + "/" + os.path.basename(customWpsiPath)
            shutil.copy(customWpsiPath, tempWpsiPath)
        else:
            if not os.path.exists(os.path.dirname(customWpsiPath)):
                os.makedirs(os.path.dirname(customWpsiPath))
            self.log.d(self.TAG, "setDartName=>copy origin file to custom directory.")
            shutil.copy(originWpsiPath, customWpsiPath)

        try:
            content = None
            with open(customWpsiPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customWpsiPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    isInFunction = False
                    count = 0
                    for line in content:
                        if isInFunction:
                            if hasCustomFile:
                                if line.strip().startswith('return "') and line.strip().endswith('";'):
                                    file.write('            return "' + name + '";\n')
                                else:
                                    file.write(line)
                            else:
                                if line.strip().startswith('return prefix + postfix;'):
                                    file.write('            // return prefix + postfix;\n')
                                    file.write('            return "' + name + '";\n')
                                else:
                                    file.write(line)
                        else:
                            file.write(line)
                            if line.strip().startswith('private String getPersistedDeviceName() {'):
                                isInFunction = True
                                count += 1
                            elif isInFunction and line.strip().endswith("{"):
                                count += 1
                            elif isInFunction and count > 0 and line.strip().endswith("}"):
                                count -= 1
                                if count == 0:
                                    isInFunction = False

                result = True
        except:
            self.log.e(self.TAG, "setDartName=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempWpsiPath):
                    shutil.copy(tempWpsiPath, customWpsiPath)
            else:
                if os.path.exists(customWpsiPath):
                    os.remove(customWpsiPath)
            
        if tempWpsiPath is not None and os.path.exists(tempWpsiPath):
            os.remove(tempWpsiPath)

        return result