# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/11/30 14:09'
import sys
import requests
import requests.adapters
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class fnDiscount(object):
	def __init__(self):
		# 订单查询接口
		self.order_query_url = 'http://erp-api.beta1.fn/cs_order_query_api/query_list'
		# 行销活动“详” 查询(分摊2，自营详)
		self.get_activity_url = 'http://erp-api.beta1.fn/cs_order_query_api/get_activity_data'

		self.query_data = {
			'STK_COUNTRY': 'cn',
			'STK_COUNTRY_REGION': 'sh',
		}

		self.s = requests.Session()
		# 增加失败请求重试次数
		retry = requests.adapters.HTTPAdapter(max_retries=3)
		self.s.mount('http://', retry)
		self.s.mount('https://', retry)

	# 获取订单详情
	def get_order_detail(self, CP):
		if not isinstance(CP, str):
			raise TypeError('订单编号须为字符串！')
		if len(CP) != 16:
			raise ValueError('订单编号须为16位！')
		CONumb = CP.replace('P', 'O')
		self.query_data['data'] = '{"OG_SEQ":"%s","CONTAIN_MALL":"1"}' % CONumb
		resp = self.s.post(url=self.order_query_url, data=self.query_data)
		return resp.json()

	# 获取自营分摊
	@classmethod
	def get_list_data(cls, CP):
		# 自营keys
		list_data_keys = ('BONUS_BY_LIST', 'SCORE_DISCOUNT', 'USE_BALANCE_POINTS', 'PCS_DISCOUNT',
		                  'USE_BALANCEPOINTS', 'USE_FULLDIS_POINTS')
		# 获取所有自营商品数据
		listDataDetail = fnDiscount().get_order_detail(CP)['Body']['list_data']
		# 筛选需要计算的key
		selfShareData = [i[j] for i in listDataDetail for j in list_data_keys if j in i.keys()]
		# 计算自营分摊总和
		return sum([float(_) for _ in selfShareData if _ is not None and _ != ''])

	# 获取商城分摊
	@classmethod
	def get_list_data_mall(cls, CP):
		# 商城keys
		list_data_mall_keys = ('APRNVOUCHER', "PLATFORMAPRNVOUCHER", 'USE_BALANCEPOINTS', 'APRNCASHCARD',
		                       'SCORE_DISCOUNT')
		# 获取所有商城商品数据
		listDataMallDetail = fnDiscount().get_order_detail(CP)['Body']['list_data_mall']
		# 筛选需要计算的key
		shopMallData = [i[j] for i in listDataMallDetail for j in list_data_mall_keys if j in i.keys()]
		# 计算商城分摊总和
		return sum([float(_) for _ in shopMallData if _ is not None and _ != ''])

	def assert_discount_detail(self, CP):
		assert fnDiscount.get_list_data(CP)


if __name__ == '__main__':
	# 分摊1 201612CP01100435  分摊2：201612CP02100675

	print(fnDiscount.get_list_data('201612CP02100675'))
	print(fnDiscount.get_list_data_mall('201612CP02100675'))
