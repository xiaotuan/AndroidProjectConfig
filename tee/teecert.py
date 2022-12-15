import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class TeeCert:
    """
    处理 cert.dat 文件

    默认处理方法：
        将 cert.dat 文件拷贝至 vendor/mediatek/proprietary/trustzone/trustkernel/source/build/公版名称/ 目录下
    """

    TAG = "TeeCert"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def setCertFile(self, file):
        """
        设置 cert.dat 文件
        """
        result = False
        if os.path.exists(file):
            hasCustomFile = False
            customCertPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/trustzone/trustkernel/source/build/" + self.info.publicName + "/cert.dat"
            try:
                if os.path.exists(customCertPath):
                    hasCustomFile = True
                    tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customCertPath)
                    shutil.copy(customCertPath, tempBuildinfoPath)

                shutil.copy(file, customCertPath);
                result = True
            except:
                self.log.e(self.TAG, "setArrayFile=>error: " + traceback.format_exc())
                if hasCustomFile:
                    if os.path.exists(tempBuildinfoPath):
                        shutil.copy(tempBuildinfoPath, customCertPath)
                else:
                    if os.path.exists(customCertPath):
                        os.remove(customCertPath)
                
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)
        return result