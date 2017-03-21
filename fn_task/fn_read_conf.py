# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/9 12:30'
import os
from configparser import ConfigParser


# 装饰器，实现账号使用N次后更换下一个账号
def mark_info(func):
	def wrapper(filepath):
		usersINFO, cfg = func(filepath)
		mark_numb = int(cfg.get('mark_numb', 'counts'))
		mark_line = int(cfg.get('mark_line', 'line'))
		total_user = len(usersINFO)
		if mark_line < total_user - 1:
			if mark_numb >= 2:
				cfg.set("mark_numb", "counts", str(1))
				cfg.set("mark_line", "line", str(mark_line + 1))
				with open(filepath, 'w+') as fp:
					cfg.write(fp)
				mark_line = int(cfg.get('mark_line', 'line'))
				return usersINFO[mark_line][-1].split(',')
			if mark_numb < 2:
				cfg.set("mark_numb", "counts", str(mark_numb + 1))
				with open(filepath, 'w+') as fp:
					cfg.write(fp)
				return usersINFO[mark_line][-1].split(',')
			else:
				return None
		if mark_line == total_user - 1:
			cfg.set("mark_line", "line", str(0))
			cfg.set("mark_numb", "counts", str(0))
			with open(filepath, 'w+') as fp:
				cfg.write(fp)
			return usersINFO[total_user - 1][-1].split(',')
		else:
			return None

	return wrapper


class readUserInfo(object):
	# @staticmethod
	# def is_conf_exist(CPath=None, user=None, psw=None, paypsw=None):
	# 	if user is not None:
	# 		return user, psw, paypsw
	# 	if CPath is not None:
	# 		if not os.path.isfile(CPath):
	# 			return '文件不存在：{}'.format(CPath)
	# 		return CPath
	# 	if not (CPath and user and psw and paypsw):
	# 		return 'ellen_001', 'xie0723', 'xie0723'

	@staticmethod
	def is_conf_exist(CPath=None, user=None, psw=None, paypsw=None):
		if CPath:
			if not os.path.isfile(CPath):
				return '文件不存在：{}'.format(CPath)
			return CPath

		if not CPath:
			user = user or 'ellen_001'
			psw = psw or 'xie0723'
			paypsw = paypsw or 'xie0723'
			return user, psw, paypsw

	@staticmethod
	@mark_info
	def read_conf_info(filepath):
		cfg = ConfigParser()
		cfg.read(filepath)
		try:
			return cfg.items('userInfo'), cfg
		except Exception as e:
			print(e)


ini_path = 'd:/coding/fn_work/fn_config.ini'
readUserInfo_ = readUserInfo()

# Test
# 配置文件存在，返还配置文件路径
# a = (readUserInfo_.is_conf_exist(ini_path))

# 配置文件不存在，并且不传入user，psw，paypsw，返还默认的user，psw，paypsw
# a, b, c = readUserInfo_.is_conf_exist()

# 配置文件不存在，并且传入了user，psw，paypsw，返回传入的值
a, b, c = readUserInfo_.is_conf_exist(user='a', psw='b', paypsw='c')

userINFO = readUserInfo_.read_conf_info(ini_path)
# print (userINFO.next())
# print(userINFO)
# a, b, c = list((userINFO.next()))
print (a, b, c)
