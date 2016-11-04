# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/31 17:12'

import requests

# 获取beta 账号的guid

url_beta = 'http://mem-info.beta1.fn:8080/member_api/searchMember'
url_preview = 'http://mem-info.idc1.fn:8080/member_api/searchMember'

query_data = {
	'name': '13545379728',
	'type': 2  # 1:email查 2 用手机查 3:用飞牛用户名查 5 用guid查
}

resp = requests.post(url_beta, data=query_data, verify=False)
print resp.json()['data']['MEM_GUID']
