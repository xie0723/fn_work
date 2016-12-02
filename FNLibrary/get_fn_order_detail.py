# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/11/30 14:09'
import sys
import requests
import requests.adapters

reload(sys)
sys.setdefaultencoding('utf-8')


class fnDiscount(object):
	def __init__(self):
		# 订单查询接口
		self.order_query_url = 'http://erp-api.beta1.fn/cs_order_query_api/query_list'
		self.query_data = {
			'STK_COUNTRY': 'cn',
			'STK_COUNTRY_REGION': 'sh',
		}
		self.s = requests.Session()
		# 增加失败请求重试次数
		retry = requests.adapters.HTTPAdapter(max_retries=3)
		self.s.mount('http://', retry)
		self.s.mount('https://', retry)

	def get_fn_order_detail(self, CP):
		if not isinstance(CP, str):
			raise TypeError('Expected a string')
		elif len(CP) < 16:
			raise Exception('订单编号须为16位')
		CONumb = CP.replace('P', 'O')
		self.query_data['data'] = '{"OG_SEQ":"%s","CONTAIN_MALL":"1"}' % CONumb
		resp = self.s.post(url=self.order_query_url, data=self.query_data)
		return resp.json()

	def get_fn_discount_detail(self):
		pass

if __name__ == '__main__':
	fnDiscount().get_fn_order_detail('201612CP01100435')
