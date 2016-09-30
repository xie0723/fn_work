# -*- coding: utf-8 -*-
import requests

__Author__ = "xiewm"
__Date__ = '2016/9/29 11:31'

url = 'http://10.202.249.188:8080/partner/api/del-white-list.json'
proxies = {
	'http': 'http://proxy2.fn.com:8080',
	'https': 'http://proxy2.fn.com:8080'
}


def unbinding_fn_partner(proxy=None):
	if not proxy:
		resp = requests.post(url)
		return resp.text
	else:
		return requests.post(url, proxies=proxies).text

print(unbinding_fn_partner())
