import unittest
import time
import sys
sys.path.append(r"./codes/utils")
from time_utils import *

class TestTimeUtils(unittest.TestCase):
    """针对 time_utils 模块的测试"""

    def test_get_log_time(self):
        """测试 time_utils 模块中的 get_log_time() 方法"""
        self.assertEqual(get_log_time(), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    
unittest.main()