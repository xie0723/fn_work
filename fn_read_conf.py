# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/9 12:30'
import os
from configparser import ConfigParser


# 装饰器，实现账号使用10次后更换下一个
def mark_users_number(func):
	def wrapper(self):
		usernames, psws, paypsws = func(self)
		if usernames == 'autotest1@autotest.com':
			yield usernames, psws, paypsws
		else:
			for i in range(len(usernames)):
				mark = 0
				while mark < 3:
					mark += 1
					yield usernames[i], psws[i], paypsws[i]
	return wrapper


class readUserInfo_(object):
	def __init__(self):
		self.cfg = ConfigParser()

	@staticmethod
	def is_conf_exist(CPath=None, user=None, psw=None, paypsw=None):
		if CPath is None and user is None and psw is None and paypsw is None:
			return 'ellen_001', 'xie0723'
		if user is not None and psw is not None and paypsw is not None:
			return user, psw, paypsw
		if CPath is not None:
			if not os.path.isfile(CPath):
				return '文件不存在：{}'.format(CPath)
			return CPath, 1, 1

	def read_conf_info(self, filepath):
		self.cfg.read(filepath)
		try:
			usernames = self.cfg.get('userInfo', 'username').strip().split(',')
			psws = self.cfg.get('userInfo', 'password').strip().split(',')
			paypsws = self.cfg.get('userInfo', 'cardSecurePass').strip().split(',')
			return usernames, psws, paypsws
		except Exception as e:
			print(e)




def aa(fp):
	print (fp.read())

ini_path = 'd:/coding/fn_work/fn_config.ini'
readUserInfo_ = readUserInfo_()
a, b, c = (readUserInfo_.is_conf_exist(ini_path))
print (readUserInfo_.read_conf_info(a))

print (a, b, c)
