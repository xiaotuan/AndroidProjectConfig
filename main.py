import platform
import time

from codes.settings.settings import Settings
from codes.log.log import Log
from codes.universal_property import UniversalProperty
from codes.version import Version
from codes.base_settings import BaseSettings

tag = 'Main'
log = Log()
start_time = time.time()

if __name__ != '__main__':
    # 脚本被当做文件运行
    log.e(tag, "脚本不是以文件方式执行，退出程序!!!\n")
    exit(-1)

if platform.system() != 'Linux':
    log.e(tag, "脚本必须运行在 Linux 系统下!!!\n")
    exit(-2)

# 执行结果
exec_result = True
# 保存修改文件数组
modify_files = []
# 修改失败文件数组
modify_fail_files = []
# 保存测试结果字典
results = {}
# 配置对象
settings = Settings()

# 修改软件版本号对象
version = Version(settings, results, modify_files, modify_fail_files, log)
# 修改通用属性对象
universalProperty = UniversalProperty(settings, results, modify_files, modify_fail_files, log)
# 修改基本设置对象
baseSettings = BaseSettings(settings, results, modify_files, modify_fail_files, log)

# 打印工程配置信息
log.i(tag, "==============================================================")
log.i(tag, "Project Path: " + settings.project_path)
log.i(tag, "Custom Folder Path: " + settings.custom_folder_path)
log.i(tag, "Android Version: " + settings.android_version)
log.i(tag, "Platform: " + settings.platform)
log.i(tag, "Chip: " + settings.chip)
log.i(tag, "GMS: " + str(settings.gms))
log.i(tag, "GMS GO: " + str(settings.gms_go))
log.i(tag, "GMS 2G GO: " + str(settings.gms_2g_go))
log.i(tag, "Public Version Name: " + settings.public_version_name)
log.i(tag, "Drive Folder Name: " + settings.drive_directory_name)
log.i(tag, "Custom Folder Name: " + settings.custon_directory_name)
log.i(tag, "Task Number: " + settings.task_number)
log.i(tag, "==============================================================")


# 修改软件版本号
version.exec()
# 修改通用属性
universalProperty.exec()
# 修改基本设置
baseSettings.exec()


# 输出修改文件列表
log.i(tag, "")
log.i(tag, "======================= Modify files =========================")
for item in modify_files:
    log.i(tag, item)
if len(modify_files) == 0:
    log.i(tag, "")
log.i(tag, "==============================================================")

# 输出修改文件列表
log.i(tag, "")
log.i(tag, "===================== Modify fail files ======================")
for item in modify_fail_files:
    log.i(tag, item)
if len(modify_fail_files) == 0:
    log.i(tag, "")
log.i(tag, "==============================================================")

# 输出执行结果
log.i(tag, "")
log.i(tag, "========================== Result ============================")
for key, value in results.items():
    if exec_result and value['Fail'] != 0:
        exec_result = False
    log.i(tag, key + ": Total " + str(value['Total']) + ", Pass " + str(value['Pass']) + ", Fail " + str(value['Fail']))
log.i(tag, "==============================================================")

diff_time = int(time.time() - start_time)
hour = diff_time / (60 * 60)
minute = (diff_time - diff_time % (60 * 60)) / 60
second = diff_time % 60
use_time = str(int(hour)) + " hour " + str(int(minute)) + " minute " + str(second) + " second"
log.i(tag, "")
if exec_result:
    log.i(tag, "Exec success, use time: " + use_time)
else:
    log.i(tag, "Exec fail, use time: " + use_time)
log.i(tag, "")