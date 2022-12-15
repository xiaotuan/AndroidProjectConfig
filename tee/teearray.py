import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class TeeArray:
    """
    处理 array.c 文件

    默认处理方法：
        将 array.c 文件拷贝至 vendor/mediatek/proprietary/trustzone/trustkernel/source/build/公版名称/ 目录下
    """

    TAG = "TeeArray"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def setArrayFile(self, file):
        """
        设置 array.c 文件
        """
        result = False
        if os.path.exists(file):
            hasCustomFile = False
            customArrayPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/trustzone/trustkernel/source/build/" + self.info.publicName + "/array.c"
            try:
                if os.path.exists(customArrayPath):
                    hasCustomFile = True
                    tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customArrayPath)
                    shutil.copy(customArrayPath, tempBuildinfoPath)

                shutil.copy(file, customArrayPath);
                result = True
            except:
                self.log.e(self.TAG, "setArrayFile=>error: " + traceback.format_exc())
                if hasCustomFile:
                    if os.path.exists(tempBuildinfoPath):
                        shutil.copy(tempBuildinfoPath, customArrayPath)
                else:
                    if os.path.exists(customArrayPath):
                        os.remove(customArrayPath)
                
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)
        return result