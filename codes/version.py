import shutil
import os
import traceback

class Version():
    """
    用于配置软件版本号类
    修改文件列表如下：
        build/make/tools/buildinfo.sh
        索麦项目还需要修改如下文件：
        build/make/core/build_id.mk
        build/make/core/sysprop.mk
    """

    def __init__(self, settings, results, modify_files, modify_fail_files, log):
        self.log = log
        self.tag = 'Version'
        self.results = results
        self.settings = settings
        self.modify_files = modify_files
        self.modify_fail_files = modify_fail_files
        self.total = 1
        if self.settings.task_number == '134':
            self.total = 3
        if self.settings.modify_version:
            self.results['Version'] = {
                'Total': self.total,
                'Pass' : 0,
                'Fail' : self.total
            }
        else:
            self.results['Version'] = {
                'Total': 0,
                'Pass' : 0,
                'Fail' : 0
            }


    def exec(self):
        """执行修改版本号"""
        self.log.d(self.tag, "[exec] 正在修改软件版本号...")
        if self.settings.modify_version:
            if self.settings.android_version == '11':
                self.modifyAndoird11Version()
            elif self.settings.android_version == '12':
                self.modifyAndroid12Version()

    
    def modifyAndoird11Version(self):
        """修改 Android 11 的版本号"""
        self.log.e(self.tag, "[modifyAndoird11Version] 暂未实现该功能...")
        raise Exception("修改 Android 11 版本号功能未实现！！！")


    def modifyAndroid12Version(self):
        """
        修改 Android 12 的版本号
        修改方法如下：
        修改 build/make/tools/buildinfo.sh 文件中的如下代码：
        echo "ro.build.display.id=ML_SO0N_M10_4G_T3.GOV.V2_`date +%Y%m%d`"
        """
        if self.settings.task_number == '134':
            if self.modifyBuildInfoFile():
                self.results['Version']['Pass'] += 1
                self.results['Version']['Fail'] -= 1
                self.modify_files.append(self.getCustomBuildInfoFilePath())
            else:
                self.modify_fail_files.append(self.getCustomBuildInfoFilePath())

            if self.modifyBuildIdFile():
                self.results['Version']['Pass'] += 1
                self.results['Version']['Fail'] -= 1
                self.modify_files.append(self.getCustomBuildIdFilePath())
            else:
                self.modify_fail_files.append(self.getCustomBuildIdFilePath())
            
            if self.modifySyspropFile():
                self.results['Version']['Pass'] += 1
                self.results['Version']['Fail'] -= 1
                self.modify_files.append(self.getCustomSyspropFilePath())
            else:
                self.modify_fail_files.append(self.getCustomSyspropFilePath())
        else:
            if self.modifyBuildIdFile():
                self.results['Version']['Pass'] += 1
                self.results['Version']['Fail'] -= 1
                self.modify_files.append(self.getCustomBuildInfoFilePath())
            else:
                self.modify_fail_files.append(self.getCustomBuildInfoFilePath())


    def modifyBuildInfoFile(self):
        """
        修改 buildinfo.sh 文件
        1. build/make/tools/buildinfo.sh 中的如下代码：

            echo "ro.build.display.id=ML_SO0N_M10_4G_T3.GOV.V4_$(date +%Y%m%d)"

            索麦项目还需要修改下面代码：

            echo "ro.build.version.incremental=2"

            ro.build.version.incremental 的值为对应的版本号
        """
        file_path = self.getBuildInfoFilePath()
        custom_file_path = self.getCustomBuildInfoFilePath()
        self.log.d(self.tag, "[modifyBuildInfoFile] buildinfo.sh file path: " + file_path)
        self.log.d(self.tag, "[modifyBuildInfoFile] custom buildinfo.sh file path: " + custom_file_path)

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return False

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return False

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
                    if self.settings.task_number == '134':
                        line = 'echo "ro.build.version.incremental=' + self.settings.version_code + '"\n'
                        find_incremental = True
                elif "date=$(date +%Y%m%d)\n" == line:
                    continue
                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifyBuildInfoFile] find_versin: " + str(find_versin) + ", find_incremental: " + str(find_incremental))
            if self.settings.task_number == '134':
                return find_versin and find_incremental
            else:
                return find_versin
        except Exception as e:
            self.log.d(self.tag, "[modifyBuildInfoFile] error: " + traceback.format_exc())
            return False


    def modifyBuildIdFile(self):
        """
        修改 build_id.mk 文件（当前该文件修改只针对 Android 12 索麦 134 项目）

        1. build/make/core/build_id.mk

        BUILD_ID=GOV.V2_$$($(DATE_FROM_FILE) +%Y%m%d)

        """
        file_path = self.getBuidIdFilePath()
        custom_file_path = self.getCustomBuildIdFilePath()
        self.log.d(self.tag, "[modifyBuildIdFile] build_id.mk file path: " + file_path)
        self.log.d(self.tag, "[modifyBuildIdFile] custom build_id.mk file path: " + custom_file_path)

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return False

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return False

            # 读取 build_id.mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 build_id.mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 build_id.mk 内容并写回文件中
            find_buildid = False
            for line in lines:
                if "BUILD_ID=" in line:
                    line = 'BUILD_ID=GOV.V' + self.settings.version_code + '_$$($(DATE_FROM_FILE) +%Y%m%d)\n'
                    find_buildid = True
                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifyBuildIdFile] find_buildid: " + str(find_buildid))
            return find_buildid
        except Exception as e:
            self.log.d(self.tag, "[modifyBuildIdFile] error: " + traceback.format_exc())
            return False


    def modifySyspropFile(self):
        """
        修改 sysprop.mk 文件（当前该文件修改只针对 Android 12 索麦 134 项目）

        1. build/make/core/sysprop.mk

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
        file_path = self.getSyspropFilePath()
        custom_file_path = self.getCustomSyspropFilePath()
        self.log.d(self.tag, "[modifySyspropFile] sysprop.mk file path: " + file_path)
        self.log.d(self.tag, "[modifySyspropFile] custom sysprop.mk file path: " + custom_file_path)
        file_exsits = True

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return False

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)
                file_exsits = False

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return False

            # 读取 sysprop.mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 sysprop.mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 sysprop.mk 内容并写回文件中
            find_sysprop = False
            find_sysprop2 = False
            for line in lines:
                if 'echo "ro.system.build.id=GOV.V' in line:
                    line = '\t\techo "ro.system.build.id=GOV.V' + self.settings.version_code + '_`$(DATE_FROM_FILE) +%Y%m%d`" >> $(2);\\\n' 
                    find_sysprop = True
                elif 'echo "ro.$(1).build.id=$(BUILD_ID)" >> $(2);' in line and (not file_exsits):
                    line = '    $(if $(filter system,$(1)),\\\n' 
                    line += '\t\techo "ro.system.build.id=GOV.V' + self.settings.version_code + '_`$(DATE_FROM_FILE) +%Y%m%d`" >> $(2);\\\n' 
                    line += '\t  ,\\\n' 
                    line += '\t\techo "ro.$(1).build.id=$(BUILD_ID)" >> $(2);\\\n'
                    line += '\t)\\\n'
                    find_sysprop = True
                elif 'ro.$(1).build.version.incremental=' in line:
                    line = '    echo "ro.$(1).build.version.incremental=' + self.settings.version_code + '" >> $(2);\\\n'
                    find_sysprop2 = True
                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifySyspropFile] find_sysprop: " + str(find_sysprop) + ", find_sysprop2: " + str(find_sysprop2))
            return find_sysprop and find_sysprop2
        except Exception as e:
            self.log.d(self.tag, "[modifySyspropFile] error: " + traceback.format_exc())
            return False


    def getBuildInfoFilePath(self):
        """获取版本号文件路径"""
        return self.settings.project_path + "/build/make/tools/buildinfo.sh"

    
    def getCustomBuildInfoFilePath(self):
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