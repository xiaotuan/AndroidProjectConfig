import os
import time
import traceback
import shutil

from constant import TEMP_DIR_NAME


class BtName:
    """
    蓝牙名称处理类

    默认处理方法：
        修改 system/bt/btif/src/btif_dm.cc 方法中的如下代码：
            static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX  1] = {'\0'};
    """


    TAG = "BtName"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getBluetoothName(self):
        """
        获取蓝牙名称
        """
        name = ""
        customBtifPath = self.info.customDir + "/alps/system/bt/btif/src/btif_dm.cc"
        if os.path.exists(customBtifPath):
            with open(customBtifPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.strip().startswith('static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = "') and line.strip().endswith('";'):
                        self.log.d(self.TAG, "getBluetoothName=>line: " + line)
                        name = line.strip()[len('static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = "'):len(line)]
                        name = name[0:(len(name) - len('";'))]
        self.log.d(self.TAG, "getBluetoothName=>name: " + name)
        return name


    def setBluetoothName(self, name):
        """
        设置蓝牙名称

        Parameters:
            name - 蓝牙名称
        """
        self.log.d(self.TAG, "setBluetoothName=>name: " + name)
        result = False
        hasCustomFile = False
        tempBtifPath = None
        originBtifPath = self.info.projectDir + "/system/bt/btif/src/btif_dm.cc"
        customBtifPath = self.info.customDir + "/alps/system/bt/btif/src/btif_dm.cc"
        if os.path.exists(customBtifPath):
            hasCustomFile = True
            tempBtifPath = TEMP_DIR_NAME + "/" + os.path.basename(customBtifPath)
            shutil.copy(customBtifPath, tempBtifPath)
        else:
            if not os.path.exists(os.path.dirname(customBtifPath)):
                os.makedirs(os.path.dirname(customBtifPath))
            shutil.copy(originBtifPath, customBtifPath)

        try:
            content = None
            with open(customBtifPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customBtifPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if hasCustomFile and line.strip().startswith('static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = "'):
                            file.write('static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = "' + name + '";\n')
                        elif not hasCustomFile and line.strip().startswith("static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] ="):
                            file.write("// static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = {'\\0'};")
                            file.write('static char btif_default_local_name[DEFAULT_LOCAL_NAME_MAX + 1] = "' + name + '";\n')
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setMode=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBtifPath):
                    shutil.copy(tempBtifPath, customBtifPath)
            else:
                if os.path.exists(customBtifPath):
                    os.remove(customBtifPath)
            
        if tempBtifPath is not None and os.path.exists(tempBtifPath):
            os.remove(tempBtifPath)

        return result