# -*- coding: utf-8 -*-
import requests

__Author__ = "xiewm"
__Date__ = '2016/9/29 11:31'

# beta 解绑合伙人
url_beta = 'http://10.202.249.188:8080/partner/api/del-white-list.json'
# preview 解绑合伙人
url_preview = 'http://partner.idc1.fn/partner/api/del-white-list.json'
proxies = {
	'http': 'http://proxy2.fn.com:8080',
	'https': 'http://proxy2.fn.com:8080'
}


# 解绑手机绑定的合伙人
def unbinding_fn_partner(url, proxy=None):
	if not proxy:
		resp = requests.post(url)
		return resp.text
	else:
		return requests.post(url, proxies=proxies).text


# print(unbinding_fn_partner(url_preview))
# -------------------------------------------------------------------------------------------
# 解绑身份证或工会会员编号绑定的合伙人
beta1_url = 'http://mem-info.beta1.fn:8080/thirdparty_login_api/unbind'
preview_url = 'http:///mem-info.idc1.fn/thirdparty_login_api/unbind'

Id = [320501199105025546, 320682199108034337, 320321199007281444, 320525198906118319, 320586199202052953,
      320503199203252016, 320586199301266615]

identifier = ['FN13681702812', 'FN18817350541', 'FN13524485369', 'FN13681702810', 'FN13003258711']


def unbinding_fn_id_partner(url):
	unbind_data = {
		'memGuid': ' ',
		'openType': 10,  # 14 是上海工会，14是苏州工会
		'openId': 'FN13003258711',
		'appId': '-'
	}
	text = requests.post(url, unbind_data).text
	print(text)


unbinding_fn_id_partner(url=beta1_url)
