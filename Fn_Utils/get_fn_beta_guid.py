# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/31 17:12'

import requests

url = 'http://mem-info.beta1.fn:8080/member_api/searchMember'


# 获取beta上面的账号guid
def get_guid(params, type_=1):
	query_data = {
		'name': params,
		'type': type_  # 1:email查 2 用手机查 3:用飞牛用户名查 5 用guid查
	}
	resp = requests.post(url, data=query_data, verify=False)

	print resp.json()['data']['MEM_GUID']


get_guid('13545379728', 2)
