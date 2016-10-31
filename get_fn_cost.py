# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/27 14:29'
import requests


class getCostInfo(object):
	def __init__(self):
		self.domain_name = 'http://pmadmin-api.beta1.fn'
		# 获取每个商品成本
		self.addr = '/erp_show_api/get_show_main_for_erp'
		self.session = requests.Session()
		self.session.verify = False

	def get_cost(self):
		query_dates = {
			'data': '{"sm_seq":"201608CM260000173"}',
			'STK_COUNTRY': 'cn',
			'STK_COUNTRY_REGION': 'sh'
		}

		resp = self.session.post(url=(self.domain_name + self.addr), data=query_dates)
		print type(resp.json()['Body']['data'])
		print float((resp.json()['Body']['data'][0]['IT_SHOW_COST']))
