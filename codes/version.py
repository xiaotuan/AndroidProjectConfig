import shutil
import os

class Version():
    """
    用于配置软件版本号类
    """

    def __init__(self, settings, results, modify_files, log):
        self.log = log
        self.tag = 'Version'
        self.results = results
        self.settings = settings
        self.modify_files = modify_files
        if self.settings.modify_version:
            self.results['Version'] = {
                'Total': 1,
                'Pass' : 0,
                'Fail' : 0,
                'Not performed' : 1
            }
        else:
            self.results['version'] = {
                'Total': 0,
                'Pass' : 0,
                'Fail' : 0,
                'Not performed' : 0
            }


    def exec(self):
        """执行修改版本号"""
        self.log.d(self.tag, "[exec] 正在修改软件版本号...")
        if self.settings.modify_version:
            if self.settings.android_version == '11':
                self.modifyAndoird11Version()
            elif self.settings.android_version == '12':
                self.modifyAndroid12Version()
            else:
                self.results['Version'] = {
                    'Total': 1,
                    'Pass' : 0,
                    'Fail' : 1,
                    'Not performed' : 0
                }

    
    def modifyAndoird11Version(self):
        """修改 Android 11 的版本号"""
        self.log.e(self.tag, "[modifyAndoird11Version] 暂未实现该功能...")
        self.results['Version'] = {
                    'Total': 1,
                    'Pass' : 0,
                    'Fail' : 1,
                    'Not performed' : 0
                }


    def modifyAndroid12Version(self):
        """
        修改 Android 12 的版本号
        修改方法如下：
        修改 build/make/tools/buildinfo.sh 文件中的如下代码：
        echo "ro.build.display.id=ML_SO0N_M10_4G_T3.GOV.V2_$(date +%Y%m%d)"
        """
        if self.settings.task_number == '134':
            self.modifySouMaiVersion()
        else:
            file_path = self.getVersionFilePath()
            custom_file_path = self.getCustomVersionFilePath()
            self.log.d(self.tag, "[modifyAndroid12Version] buildinfo.sh file path: " + file_path)
            self.log.d(self.tag, "[modifyAndroid12Version] custom buildinfo.sh file path: " + custom_file_path)
            try:
                # 如果客制化目录中没有对应的文件则将文件拷贝至客制化目录再修改
                if not os.path.exists(custom_file_path):
                    shutil.copyfile(file_path, custom_file_path)
                # 读取 buildinfo.sh 文件内容
                file = open(custom_file_path)
                lines = file.readlines()
                file.close()
                # 重新以覆盖的方式打开 buildinfo.sh 文件
                file = open(custom_file_path, mode='w', encoding='utf8')
                # 修改 buildinfo.sh 内容并写回文件中
                find_versin = False
                for line in lines:
                    #self.log.d(self.tag, "[modifyAndroid12Version] line: " + line)
                    if line.count("ro.build.display.id=") != 0:
                        #self.log.d(self.tag, "[modifyAndroid12Version] modify version...")
                        line = 'echo "ro.build.display.id=' + self.settings.version + '"\n'
                        find_versin = True
                    file.write(line)
                file.flush()
                file.close()
                self.modify_files.append(custom_file_path)
                if find_versin:
                    self.results['Version'] = {
                                'Total': 1,
                                'Pass' : 1,
                                'Fail' : 0,
                                'Not performed' : 0
                            }
            except Exception as e:
                self.log.e(self.tag, "[modifyAndoird12Version] error: " + str(e))
                # 修改失败，删除拷贝文件
                if os.path.exists(custom_file_path):
                    os.remove(custom_file_path)
                self.results['Version'] = {
                            'Total': 1,
                            'Pass' : 0,
                            'Fail' : 1,
                            'Not performed' : 0
                        }

    
    def modifySouMaiVersion(self):
        """
        索麦项目修改需要如下文件：
        1. build/make/tools/buildinfo.sh 中的如下代码：

            echo "ro.build.display.id=ML_SO0N_M10_4G_T3.GOV.V4_$(date +%Y%m%d)"
            echo "ro.build.version.incremental=2"

            ro.build.version.incremental 的值为对应的版本号
        
        2. build/make/core/build_id.mk

            BUILD_ID=GOV.V2_$$($(DATE_FROM_FILE) +%Y%m%d)

        3. build/make/core/sysprop.mk

            echo "ro.$(1).build.id=$(BUILD_ID)" >> $(2);\
            修改为：
            $(if $(filter system,$(1)),\
                    echo "ro.system.build.id=GOV.V2_`$(DATE_FROM_FILE) +%Y%m%d`" >> $(2);\
                ,\
                    echo "ro.$(1).build.id=$(BUILD_ID)" >> $(2);\
            )\
            
            echo "ro.$(1).build.version.incremental=$(BUILD_NUMBER_FROM_FILE)" >> $(2);\
            修改为：
            echo "ro.$(1).build.version.incremental=1" >> $(2);\

        """
        file_path = self.getVersionFilePath()
        custom_file_path = self.getCustomVersionFilePath()
        build_id_file_path = self.getBuidIdFilePath()
        custom_build_id_file_path = self.getCustomBuildIdFilePath()
        sysprop_file_path = self.getSyspropFilePath()
        custom_sysprop_file_path = self.getCustomSyspropFilePath()

        self.log.d(self.tag, "[modifyAndroid12Version] buildinfo.sh file path: " + file_path)
        self.log.d(self.tag, "[modifyAndroid12Version] custom buildinfo.sh file path: " + custom_file_path)
        self.log.d(self.tag, "[modifyAndroid12Version] build_id.mk file path: " + build_id_file_path)
        self.log.d(self.tag, "[modifyAndroid12Version] custom build_id.mk file path: " + custom_build_id_file_path)
        self.log.d(self.tag, "[modifyAndroid12Version] sysprop.mk file path: " + sysprop_file_path)
        self.log.d(self.tag, "[modifyAndroid12Version] custom sysprop.mk file path: " + custom_sysprop_file_path)
        try:
            # 修改 buildinfo.sh 文件
            # 如果客制化目录中没有对应的文件则将文件拷贝至客制化目录再修改
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)
            # 读取 buildinfo.sh 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 buildinfo.sh 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 buildinfo.sh 内容并写回文件中
            find_versin = False
            find_incremental = False
            for line in lines:
                if line.count("ro.build.display.id=") != 0:
                    line = 'echo "ro.build.display.id=' + self.settings.version + '"\n'
                    find_versin = True
                elif line.count("ro.build.version.incremental=") != 0:
                    line = 'echo "ro.build.version.incremental=' + self.settings.version_code + '"\n'
                    find_incremental = True
                elif "date=$(date +%Y%m%d)\n" == line:
                    continue
                file.write(line)
            file.flush()
            file.close()

            # 修改 build_id.mk 文件
            # 如果客制化目录中没有对应的文件则将文件拷贝至客制化目录再修改
            if not os.path.exists(custom_build_id_file_path):
                shutil.copyfile(build_id_file_path, custom_build_id_file_path)
            # 读取 build_id.mk 文件内容
            file = open(custom_build_id_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 build_id.mk 文件
            file = open(custom_build_id_file_path, mode='w', encoding='utf8')
            # 修改 build_id.mk 内容并写回文件中
            find_buildid = False
            for line in lines:
                if "BUILD_ID=" in line:
                    line = 'BUILD_ID=GOV.V' + self.settings.version_code + '_$$($(DATE_FROM_FILE) +%Y%m%d)\n'
                    find_buildid = True
                file.write(line.replace('\r\n', '\n'))
            file.flush()
            file.close()

            # 修改 sysprop.mk 文件
            # 如果客制化目录中没有对应的文件则将文件拷贝至客制化目录再修改
            if not os.path.exists(custom_sysprop_file_path):
                shutil.copyfile(sysprop_file_path, custom_sysprop_file_path)
            # 读取 sysprop.mk 文件内容
            file = open(custom_sysprop_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 build_id.mk 文件
            file = open(custom_sysprop_file_path, mode='w', encoding='utf8')
            # 修改 sysprop.mk 内容并写回文件中
            find_sysprop = False
            find_sysprop2 = False
            for line in lines:
                if 'echo "ro.system.build.id=GOV.V2' in line:
                    line.replace('echo "ro.system.build.id=GOV.V2', 'echo "ro.system.build.id=GOV.V' + self.settings.version_code)
                    find_sysprop = True
                elif 'ro.$(1).build.version.incremental=' in line:
                    line = 'echo "ro.$(1).build.version.incremental=' + self.settings.version_code + '" >> $(2);\\\n'
                    find_sysprop2 = True
                file.write(line.replace('\r\n', '\n'))
            file.flush()
            file.close()

            self.setModifyResult(find_versin and find_incremental and find_buildid and find_sysprop and find_sysprop2)
        except Exception as e:
            self.log.e(self.tag, "[modifyAndoird12Version] error: " + str(e))
            self.setModifyResult(False)


    def setModifyResult(self, result):
        """设置修改结果"""
        custom_file_path = self.getCustomVersionFilePath()
        custom_build_id_file_path = self.getCustomBuildIdFilePath()
        custom_sysprop_file_path = self.getCustomSyspropFilePath()
        if result:
            self.modify_files.append(custom_file_path)
            self.modify_files.append(custom_build_id_file_path)
            self.modify_files.append(custom_sysprop_file_path)
            self.results['Version'] = {
                            'Total': 1,
                            'Pass' : 1,
                            'Fail' : 0,
                            'Not performed' : 0
                        }
        else:
            if os.path.exists(custom_file_path):
                os.remove(custom_file_path)
            if os.path.exists(custom_build_id_file_path):
                os.remove(custom_build_id_file_path)
            self.results['Version'] = {
                        'Total': 1,
                        'Pass' : 0,
                        'Fail' : 1,
                        'Not performed' : 0
                    }


    def getVersionFilePath(self):
        """获取版本号文件路径"""
        return self.settings.project_path + "/build/make/tools/buildinfo.sh"

    
    def getCustomVersionFilePath(self):
        """获取客制化版本号文件路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/build/make/tools/buildinfo.sh"


    def getBuidIdFilePath(self):
        """获取 build_id.mk 文件路径"""
        return self.settings.project_path + "/build/make/core/build_id.mk"


    def getCustomBuildIdFilePath(self):
        """获取客制化 build_id.mk 文件路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/build/make/core/build_id.mk"

    def getSyspropFilePath(self):
        """获取 sysprop.mk 文件路径"""
        return self.settings.project_path + "/build/make/core/sysprop.mk"


    def getCustomSyspropFilePath(self):
        """获取客制化 sysprop.mk 文件路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/build/make/core/sysprop.mk"