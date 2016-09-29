# coding=utf-8
__Author__ = "xiewm"
__Date__ = '2016/8/4 16:33'

import requests
import json
import socket


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
	(KHTML, like Gecko)Chrome/51.0.2704.103 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
}

register_url = 'http://member-api.beta1.fn/account_api/batchRegister'


def get_username():
	while True:
		username = str(raw_input("请输入你的注册用户名 ==>"))
		if len(username) > 6:
			break
		else:
			print (u'账号长度不能低于6位，请重新输入')
			continue
	return username


def get_password():
	while True:
		password = str(raw_input("请输入注册密码:"))
		if len(password) < 6:
			print (u'密码长度只能在6-16位字符之间，请重新输入')
			continue
		if password.isdigit() or password.isalpha():
			print (u"密码不能全部为数字或字母，请重新输入")
			continue
		else:
			break
	return password


def get_accounts_number():
	return int(raw_input("请输入需要生产的账号总数 :"))


def get_ip():
	return socket.gethostbyname(socket.gethostname())


def batch_register():
	lst = []
	user = str(get_username())
	for _ in xrange(1, get_accounts_number() + 1):
		lst.append(user + str(_))
	usernames = ','.join(lst).strip()
	print ("you userName:%s " % usernames + '\n')
	data = {
		'usernames': usernames,
		'password': get_password().strip(),
		'userinfo': '{"ip_addr":" %s"}' % get_ip()
	}
	resp = requests.post(register_url, data=data, headers=headers)
	js_resp = json.loads(resp.content)

	if '"exsitCount":0,"failcount":0,"errorUser":0' in resp.content:
		print (u'账号注册成功')
		print ("用户名为:%s " % usernames + '\n')

	if js_resp['Body']['count']['exsitCount'] > 0:
		print (u"用户已存在==》{}".format(js_resp['Body']['exsitUser']))

	if js_resp['Body']['count']['failcount'] > 0:
		print (u"用户创建失败")
		return False
	if js_resp['Body']['count']['errorUser'] > 0:
		print (u"用户名类型错误")
		return False


if __name__ == '__main__':
	batch_register()
