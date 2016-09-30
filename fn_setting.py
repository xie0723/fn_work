# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/9/30 10:56'

import os

path = os.path.abspath('fn_config.py')


def is_conf_exist(Path):
	if os.path.exists(Path):
		try:
			with open(Path) as fp:
				return fp.readlines()
		except Exception as e:
			print (e)
	else:
		return '文件不存在:{}'.format(Path)


def is_conf_exist_(Path):
	if os.path.exists(Path):
		try:
			import fn_config
			user = fn_config.user
			psw = fn_config.password
			paypsw = fn_config.cardSecurePass
			return user, psw, paypsw
		except Exception as e:
			print (e)
	else:
		return '文件不存在:{}'.format(Path)


def test():
	return is_conf_exist(path)[0]
print (is_conf_exist(path))
print (is_conf_exist_(path))
#
# print (test())
