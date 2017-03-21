# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/11/1 16:14'

import sys


def get_cur_info():
	print (sys._getframe().f_code.co_filename)  # 当前文件名
	print sys._getframe(0).f_code.co_name  # 当前函数名
	print sys._getframe(1).f_code.co_name  # 调用该函数的函数的名字，如果没有被调用，则返回module
	print sys._getframe().f_lineno  # 当前行号


def test_debug():
	get_cur_info()


test_debug()
