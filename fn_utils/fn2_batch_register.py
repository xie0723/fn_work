# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/12/14 16:37'

import requests
import socket

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

# beta2注册
register_beta2 = 'http://reg-api.beta2.fn/account_api/batchRegister'


# 获取注册用户名
def get_username():
	while True:
		username = str(raw_input("please input you username(mall phone or number+str):"))
		if len(username) > 6:
			break
		else:
			print ('username must > 6 ')
			continue
	return username


# 获取注册密码
def get_password():
	while True:
		password = str(raw_input("please input you password:"))
		if len(password) < 6:
			print('password in 6-16 please reinput ')
			continue
		elif password.isdigit() or password.isalpha():
			print ('passwords not be all numbers or letters, please re-enter:')
			continue
		else:
			break

	return password


# 获取注册账号数量
def get_accounts_number():
	return int(input('please input the number of users:'))


# 获取电脑IP地址
def get_ip():
	return socket.gethostbyname(socket.gethostname())


# 批量注册
def batch_register():
	lst = []
	user = str(get_username())
	for _ in range(1, get_accounts_number() + 1):
		lst.append(user + str(_))
	usernames = ','.join(lst).strip()
	print ("you userName:%s " % usernames + '\n')
	data = {
		'username': usernames,
		'password': get_password().strip(),
		'userInfo': '{"b2c_name":"1","ip_addr":"%s", "oauth_type":"0"}' % get_ip()
	}
	resp = requests.post(register_beta2, data=data)
	js_resp = resp.json()

	if '"failCount": 0,"exsitCount": 0,"errorCount": 0' in resp.content:
		print ('register success')
		print (u"用户名为:%s " % usernames + '\n')

	if js_resp['data']['count']['exsitCount'] > 0:
		print (u"用户已存在==》{}".format(js_resp['data']['exsitUser']))

	if js_resp["data"]['count']['failCount'] > 0:
		print (u"用户创建失败")

	if js_resp['data']['count']['errorCount'] > 0:
		print (u"用户名类型错误")


if __name__ == '__main__':
	print(u'注册时，只需要输入一个账号的起始名，之后会在名字后面加上数字标记，例如输入tester000,注册成功后的账号是tester0001,tester0002........')
	batch_register()
	raw_input(u'按任意键退出')
