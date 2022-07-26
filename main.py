import platform

from codes.settings.settings import Settings
from codes.log.log import Log
from codes.version import Version

tag = 'Main'
log = Log()

if __name__ != '__main__':
    # 脚本被当做文件运行
    log.e(tag, "脚本不是以文件方式执行，退出程序!!!\n")
    exit(-1)

if platform.system() != 'Linux':
    log.e(tag, "脚本必须运行在 Linux 系统下!!!\n")
    exit(-2)

# 保存修改文件数组
modify_files = []
# 保存测试结果字典
results = {}
# 配置对象
settings = Settings()

# 修改软件版本号对象
version = Version(settings, results, modify_files, log)

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

# 输出修改文件列表
log.i(tag, "")
log.i(tag, "======================= Modify files =========================")
for item in modify_files:
    log.i(tag, item)
log.i(tag, "==============================================================")

# 输出执行结果
log.i(tag, "")
log.i(tag, "========================== Result ============================")
for key, value in results.items():
    log.i(tag, key + ": Total " + str(value['Total']) + ", Pass " + str(value['Pass']) + ", Not performed: " + str(value['Not performed']))
log.i(tag, "==============================================================")