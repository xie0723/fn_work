# -*- coding: utf-8 -*-
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 为您推荐
# url = 'http://buy.beta1.fn/searchApi/getBuyMoreList?'

# 猜您喜欢
url = 'http://buy.beta1.fn/searchApi/getLikeGoodsList?'
resp = requests.get(url)


class getData(object):

	def get_data(self,jdata, numb=1):

		self.jdata = jdata
		self.numb = numb

		try:
			assert isinstance(jdata, dict)
		except:
			print (type(jdata))
			print ('Please check the parameter (jdata) type：%s' % jdata)

		if isinstance(jdata['info'],dict):
			dict_data = dict(
				CM=self.jdata['info']['data'][self.numb]['sm_seq'],
			)
		elif isinstance(jdata['info'],list):
			dict_data = dict(
				CM=self.jdata['info'][self.numb]['sm_seq']
			)
		else:
			print ('返回的类型错误%s'%jdata['info'])
		return dict_data
get_jdatas = getData()
print (get_jdatas.get_data(jdata=resp.json()))
