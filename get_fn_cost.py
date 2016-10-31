# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/27 14:29'
import requests

domain_name = 'http://pmadmin-api.beta1.fn'

# 获取每个商品成本
addr = '/erp_show_api/get_show_main_for_erp'

session = requests.Session()

query_dates = {
	'data': '{"sm_seq":"201511CM120000011"}',
	'STK_COUNTRY': 'cn',
	'STK_COUNTRY_REGION': 'sh'
}

resp = session.post(url=(domain_name + addr), data=query_dates, verify=False)
print float((resp.json()['Body']['data'][0]['IT_SHOW_COST']))
