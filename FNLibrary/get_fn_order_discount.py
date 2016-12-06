# -*- coding: utf-8 -*-


__Author__ = "xiewm"
__Date__ = '2016/11/30 14:09'
import sys
import requests
import requests.adapters
from functools import wraps

reload(sys)
sys.setdefaultencoding('utf-8')


# 缓存订单接口的首次查询结果
def query_order_cache(func):
	cache = {}

	@wraps(func)
	def wrapper(self, CP):
		if CP not in cache:
			cache[CP] = func(self, CP)
		return cache[CP]

	return wrapper


class fnDiscount(object):
	def __init__(self):
		# 订单明细查询
		self.order_query_url = 'http://erp-api.beta1.fn/cs_order_query_api/query_list'

		# 自营keys
		self.list_data_keys = ('BONUS_BY_LIST', 'SCORE_DISCOUNT', 'USE_BALANCE_POINTS', 'PCS_DISCOUNT',
		                       'USE_BALANCEPOINTS', 'USE_FULLDIS_POINTS')

		# 商城keys
		# self.list_data_mall_keys = ('APRNVOUCHER', "PLATFORMAPRNVOUCHER", 'USE_BALANCEPOINTS', 'APRNCASHCARD',
		#                             'SCORE_DISCOUNT')
		self.list_data_mall_keys = ('APRNPROMOTE', 'USE_BALANCEPOINTS', 'APRNCASHCARD',
		                            'SCORE_DISCOUNT')
		# 订单接口post data
		self.query_data = {
			'STK_COUNTRY': 'cn',
			'STK_COUNTRY_REGION': 'sh',
		}

		self.s = requests.Session()

	# 获取订单详情
	@query_order_cache
	def get_order_detail(self, CP):
		if len(CP) != 16:
			raise ValueError('订单编号须为16位！')
		if not isinstance(CP, str):
			raise TypeError('订单编号须为字符串！')

		CONumb = CP.replace('P', 'O')
		self.query_data['data'] = '{"OG_SEQ":"%s","CONTAIN_MALL":"1"}' % CONumb

		# 请求订单查询接口返还数据
		resp = self.s.post(url=self.order_query_url, data=self.query_data)
		return resp.json()

	# 获取自营分摊
	@classmethod
	def get_list_data(cls, CP):
		# 获取所有自营商品数据
		listDataDetail = fnDiscount().get_order_detail(CP)['Body']['list_data']

		# 筛选需要计算的key的value
		selfShareData = [i[j] for i in listDataDetail for j in fnDiscount().list_data_keys if j in i.keys()]

		# 计算自营分摊总和
		return sum([float(_) for _ in selfShareData if _ is not None and _ != ''])

	# 获取自营分摊明细
	@classmethod
	def get_list_data_detail(cls, CP):
		# 获取所有自营商品数据
		listDataDetail = fnDiscount().get_order_detail(CP)['Body']['list_data']

		# 以分摊名作为key，统计各分摊金额总计
		tempListDataDetail = {}
		for i in listDataDetail:
			for k in fnDiscount().list_data_keys:
				if k in i.keys():
					if k not in tempListDataDetail:
						tempListDataDetail[k] = (int(i[k]) if i[k] is not None and i[k] != '' else 0)
					else:
						tempListDataDetail[k] = tempListDataDetail.get(k) + (
							int(i[k]) if i[k] is None and i[k] == '' else 0)
		return tempListDataDetail

	# 获取商城分摊
	@classmethod
	def get_list_data_mall(cls, CP):
		# 获取所有商城商品数据
		listDataMallDetail = fnDiscount().get_order_detail(CP)['Body']['list_data_mall']

		# 筛选需要计算的key
		shopMallData = [i[j] for i in listDataMallDetail for j in fnDiscount().list_data_mall_keys if j in i.keys()]

		# 计算商城分摊总和
		return sum([float(_) for _ in shopMallData if _ is not None and _ != ''])

	# 获取指定商品ID的分摊
	@classmethod
	def get_ID_discount(cls, CP, *ID):
		# 获取所有自营商品数据
		listDataDetail = fnDiscount().get_order_detail(CP)['Body']['list_data']
		# 获取所有自营商品的ID_NO
		ID_NOS = [_['ID_NO'] for _ in listDataDetail]
		# print (ID_NOS)
		# 获取所有商城商品数据
		listDataMallDetail = fnDiscount().get_order_detail(CP)['Body']['list_data_mall']
		# 获取所有的商城商品ITNO
		ITNOS = [_['ITNO'] for _ in listDataMallDetail]
		# 临时字典，用于存储指定商品对应的分摊数据。
		tempDiscount = {}

		for id_ in ID:
			if id_ in ID_NOS:
				selfDiscount = [listDataDetail[ID_NOS.index(id_)][i] for i in
				                listDataDetail[ID_NOS.index(id_)].keys() for j in fnDiscount().list_data_keys
				                if j == i
				                ]

				tempDiscount[id_] = sum([float(_) for _ in selfDiscount if _ is not None and _ != ''])

			elif id_ in ITNOS:
				mallDiscount = [listDataMallDetail[ITNOS.index(id_)][i] for i in
				                listDataMallDetail[ITNOS.index(id_)].keys() for j in fnDiscount().list_data_mall_keys
				                if j == i
				                ]
				tempDiscount[id_] = sum([float(_) for _ in mallDiscount if _ is not None and _ != ''])

		return tempDiscount

	# 获取总分摊
	@classmethod
	def get_total_discount(cls, CP):
		return fnDiscount.get_list_data(CP) + fnDiscount.get_list_data_mall(CP)

	@staticmethod
	def assert_discount_detail(CP, **kwargs):

		_assert_datas01 = {
			'totalDiscount': '269.0',
			'selfDiscount': '144.92',
			'mallDiscount': '124.08',
		}
		_assert_datas = {
			'totalDiscount': '195.0',
			'selfDiscount': '86.75',
			'mallDiscount': '108.25',
		}
		return fnDiscount.get_total_discount(CP)


if __name__ == '__main__':
	# 分摊1 201612CP01100435  分摊2：201612CP02100675  行销：201612CP05101507
	print(fnDiscount.get_list_data('201612CP05101507'))
	print(fnDiscount.get_list_data_mall('201612CP05101507'))
	print(fnDiscount.get_total_discount('201612CP05101507'))
	# print(fnDiscount.assert_discount_detail('201612CP01100435'))
	# print (fnDiscount.get_list_data_detail('201612CP01100435'))
	print (fnDiscount.get_ID_discount('201612CP05101507', '201311CG150000123', '201501CG160000047', '90103162279'))
# print (fnDiscount.get_ID_discount('201612CP02100675', '201511CG120000012', '201511CG120000009'))
# print (fnDiscount.get_ID_discount('201612CP02100675', '90103163673'))
