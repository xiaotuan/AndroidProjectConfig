import time

# 不打印日志
NONE = 0
# 打印错误日志
ERROR = 1
# 打印警告和错误日志
WARN = 2
# 打印信息、警告和错误日志
INFO = 3
# 打印调试、信息、警告和错误日志
DEBUG = 4
# 打印所有日志
ALL = 5

class Log:

    def __init__(self, level):
        self.level = level


    def d(self, tag, msg):
        if self.level >= DEBUG:
            print(self.get_log_time() + " D " + tag + " : " + msg)

    
    def e(self, tag, msg):
        if self.level >= ERROR:
            print(self.get_log_time() + " E " + tag + " : " + msg)


    def w(self, tag, msg):
        if self.level >= WARN:
            print(self.get_log_time() + " W " + tag + " : " + msg)


    def i(self, tag, msg):
        if self.level >= INFO:
            print(self.get_log_time() + " I " + tag + " : " + msg)


    def get_log_time(self):
        """
        获取日志时间
        时间格式为: 2022-07-25 14:48:32
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())