import os
import shutil
import traceback

class UniversalProperty():
    """
    修改通用属性（名称、品牌、型号、制造商、设备）
    修改文件列表如下：
    device/mediateksample/tb8768p1_64_bsp/vnd_$(self.public_version_name).mk
    """

    def __init__(self, settings, results, modify_files, modify_fail_files, log):
        self.tag = 'UniversalProperty'
        self.log = log
        self.settings = settings
        self.results = results
        self.modify_files = modify_files
        self.modify_fail_files = modify_fail_files
        self.total = 0
        if self.settings.modify_universal_property:
            if self.settings.name != 'not set':
                self.total += 1
            if self.settings.brand != 'not set':
                self.total += 1
            if self.settings.model != 'not set':
                self.total += 1
            if self.settings.manufacturer != 'not set':
                self.total += 1
            if self.settings.device != 'not set':
                self.total += 1

        self.results['UniversalProperty'] = {
            'Total': self.total,
            'Pass' : 0,
            'Fail' : self.total
        }


    def exec(self):
        """
        执行修改通用属性
        """
        if self.settings.modify_universal_property and self.total > 0:
            if self.settings.android_version == '11':
                self.modifyAndroid11UniversalProperty()
            elif self.settings.android_version == '12':
                self.modifyAndroid12UniversalProperty()
            else:
                raise Exception("Unsupport modify Android " + self.settings.android_version + " base settings.")
        else:
            self.log.i(self.tag, "[exec] Set universal property is disabled or no need to modify.")


    def modifyAndroid11UniversalProperty(self):
        """
        修改 Android 11 的通用属性
        """
        raise Exception("Unsupport modify Android 11 base settings.")


    def modifyAndroid12UniversalProperty(self):
        """
        修改 Android 12 的通用属性
        """
        result = self.modifyProjectVndFile()
        self.log.d(self.tag, "[modifyAndroid12UniversalProperty] Modify Vnd file result: " + str(result))
        isSuccess = True
        for value in result.values():
            if value:
                self.results['UniversalProperty']['Pass'] += 1
                self.results['UniversalProperty']['Fail'] -= 1
            else:
                isSuccess = False
        if isSuccess:
            self.modify_files.append(self.getCustomProjectVndFilePath())
        else:
            self.modify_files.append(self.getCustomProjectVndFilePath())
    

    def modifyProjectVndFile(self):
        """
        修改 vnd_$(self.public_version_name).mk 文件
        修改代码如下：
            PRODUCT_MANUFACTURER := Sky Devices
            PRODUCT_MODEL := X8
            PRODUCT_BRAND := Sky
            PRODUCT_SYSTEM_NAME := X8
            PRODUCT_SYSTEM_DEVICE := X8
        """
        file_path = self.getProjectVndFilePath()
        custom_file_path = self.getCustomProjectVndFilePath()
        self.log.d(self.tag, "[modifyProjectVndFile] vnd file path: " + file_path)
        self.log.d(self.tag, "[modifyProjectVndFile] custom vnd file path: " + custom_file_path)
        # 返回结果，下标 0 -> name, 1 -> brand, 2 -> device, 3 -> model, 4 -> manufacturer
        result = {}
        if self.settings.name != 'not set':
            result['Name'] = False
        if self.settings.brand != 'not set':
            result['Brand'] = False
        if self.settings.model != 'not set':
            result['Model'] = False
        if self.settings.manufacturer != 'not set':
            result['Manufacturer'] = False
        if self.settings.device != 'not set':
            result['Device'] = False

        if len(result) == 0:
            self.log.w(self.tag, "[modifyProjectVndFile] No need to modify.")
            return result

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                self.log.e(self.tag, "[modifyProjectVndFile] Create vnd file parent directory failed.")
                return result

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                self.log.e(self.tag, "[modifyProjectVndFile] Copy vnd file failed.")
                return result

            # 读取 vnd_$(self.public_version_name).mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 vnd_$(self.public_version_name).mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 vnd_$(self.public_version_name).mk 内容并写回文件中
            hasSystemName = False
            hasSystemDevice = False
            for line in lines:
                if 'PRODUCT_SYSTEM_NAME' in line:
                    hasSystemName = True
                elif 'PRODUCT_SYSTEM_DEVICE' in line:
                    hasSystemDevice = True

            for line in lines:
                if 'PRODUCT_MANUFACTURER :=' in line:
                    if self.settings.manufacturer != 'not set':
                        line = 'PRODUCT_MANUFACTURER := ' + self.settings.manufacturer + '\n'
                        result['Manufacturer'] = True
                elif 'PRODUCT_MODEL :=' in line:
                    if self.settings.model != 'not set':
                        line = 'PRODUCT_MODEL := ' + self.settings.model + '\n'
                        result['Model'] = True
                elif 'PRODUCT_BRAND :=' in line:
                    if self.settings.brand != 'not set':
                        line = 'PRODUCT_BRAND := ' + self.settings.brand + '\n'
                        result['Brand'] = True
                    
                    if not hasSystemName or not hasSystemDevice:
                        line += '\n'
                        if not hasSystemName and self.settings.name != 'not set':
                            line += 'PRODUCT_SYSTEM_NAME := ' + self.settings.name + '\n'
                            result['Name'] = True
                        if not hasSystemDevice and self.settings.device != 'not set':
                            line += 'PRODUCT_SYSTEM_DEVICE := ' + self.settings.device + '\n'
                            result['Device'] = True
                        line += '\n'

                elif 'PRODUCT_SYSTEM_NAME :=' in line:
                    if self.settings.name != 'not set':
                        line = 'PRODUCT_SYSTEM_NAME := ' + self.settings.name + '\n'
                        result['Name'] = True
                elif 'PRODUCT_SYSTEM_DEVICE :=' in line:
                    if self.settings.device != 'not set':
                        line = 'PRODUCT_SYSTEM_DEVICE := ' + self.settings.device + '\n'
                        result['Device'] = True

                file.write(line)
            file.flush()
            file.close()
            return result
        except Exception as e:
            self.log.d(self.tag, "[modifyProjectVndFile] error: " + traceback.format_exc())
            if os.path.exists(self.getCustomProjectVndFilePath()):
                os.remove(self.getCustomProjectVndFilePath())
            return result


    def getProjectVndFilePath(self):
        """
        获取 vnd_$(self.public_version_name).mk 文件路径
        """
        return self.settings.project_path + "/device/mediateksample/" + self.settings.public_version_name + "/vnd_" + self.settings.public_version_name + ".mk"

    
    def getCustomProjectVndFilePath(self):
        """
        获取客制化的 vnd_$(self.public_version_name).mk 文件路径
        """
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/device/mediateksample/" + self.settings.public_version_name + "/vnd_" + self.settings.public_version_name + ".mk"
