import imp
import os
import shutil
import traceback

from codes.utils.time_utils import get_build_number

class FingerPrint():
    """
    修改 fingerprint
    修改的文件如下：
    device/mediatek/system/common/BoardConfig.mk
    """

    def __init__(self, settings, results, modify_files, modify_fail_files, log):
        self.tag = 'FingerPrint'
        self.log = log
        self.settings = settings
        self.results = results
        self.modify_files = modify_files
        self.modify_fail_files = modify_fail_files
        self.total = 0
        if self.settings.modify_fingerprint:
            if self.settings.build_number != 'not set':
                self.total = 1
        self.results['FingerPrint'] = {
            'Total': self.total,
            'Pass': 0,
            'Fail': self.total
        }

    
    def exec(self):
        """
        执行修改 fingerprint 操作
        """
        if self.settings.modify_fingerprint and self.total > 0:
            if self.settings.android_version == '11':
                self.modifyAndroid11Fingerprint()
            elif self.settings.android_version == '12':
                self.modifyAndroid12Fingerprint()
            else:
                raise Exception("Unsupport modify Android " + self.settings.android_version + "  fingerprint.")
        else:
            self.log.w(self.tag, "[exec] Set fingerprint is disabled or no need to modify.")
    

    def modifyAndroid11Fingerprint(self):
        """
        修改 Android 11 的 fingerprint
        """
        raise Exception("Unsupport modify Android 11 fingerprint.")


    def modifyAndroid12Fingerprint(self):
        """
        修改 Android 12 的 fingerprint
        """
        customFilePath = self.getCustomBoardConfigFilePath()
        result = self.modifyBoardConfigFile()
        self.log.d(self.tag, "[modifyAndroid12Fingerprint] modify BoardConfig.mk file result: " + str(result))
        isSuccess = True
        for value in result.values():
            if value:
                self.results['FingerPrint']['Pass'] += 1
                self.results['FingerPrint']['Fail'] -= 1
            else:
                isSuccess = False
        if isSuccess:
            self.modify_files.append(customFilePath)
        else:
            self.modify_files.append(customFilePath)


    def modifyBoardConfigFile(self):
        """
        修改 device/mediatek/system/common/BoardConfig.mk 文件中的如下代码：
        WEIBU_BUILD_NUMBER := $(shell date +%s)
        """
        file_path = self.getBoardConfigFilePath()
        custom_file_path = self.getCustomBoardConfigFilePath()
        self.log.d(self.tag, "[modifyBoardConfigFile] BoardConfig.mk file path: " + file_path)
        self.log.d(self.tag, "[modifyBoardConfigFile] custom BoardConfig.mk file path: " + custom_file_path)
        # 返回结果，下标 0 -> name, 1 -> brand, 2 -> device, 3 -> model, 4 -> manufacturer
        result = {}

        if self.settings.build_number != 'not set':
            result['BuildNumber'] = False

        if len(result) == 0:
            self.log.w(self.tag, "[modifyBoardConfigFile] No need to modify.")
            return result

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                self.log.e(self.tag, "[modifyBoardConfigFile] create BoardConfig.mk parent directory failed.")
                return result

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                self.log.e(self.tag, "[modifyBoardConfigFile] copy BoardConfig.mk file failed.")
                return result

            # 读取 BoardConfig.mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 BoardConfig.mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 BoardConfig.mk 内容并写回文件中
            for line in lines:
                if 'WEIBU_BUILD_NUMBER :=' in line:
                    if self.settings.build_number != 'not set':
                        if self.settings.build_number == 'now':
                            line = 'WEIBU_BUILD_NUMBER := ' + get_build_number() + '\n'
                        else:
                            line = 'WEIBU_BUILD_NUMBER := ' + self.settings.build_number + '\n'
                        result['BuildNumber'] = True

                file.write(line)
            file.flush()
            file.close()
            return result
        except Exception as e:
            self.log.d(self.tag, "[modifyBoardConfigFile] error: " + traceback.format_exc())
            if os.path.exists(self.getCustomBoardConfigFilePath()):
                os.remove(self.getCustomBoardConfigFilePath())
            return result

    
    def getBoardConfigFilePath(self):
        """
        获取 BoardConfig.mk 文件路径：
        """
        return self.settings.project_path + "/device/mediatek/system/common/BoardConfig.mk"


    def getCustomBoardConfigFilePath(self):
        """
        获取客制化 BoardConfig.mk 文件路径：
        """
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/device/mediatek/system/common/BoardConfig.mk"