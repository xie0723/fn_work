# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/8/5 17:26'

import requests

url_login = 'http://zentao.fn.com/index.php?m=user&f=login'
headers1 = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
	 Chrome/51.0.2704.103 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
}

formDataLogin = {
	'account': 'wangming.xie',
	'password': 'Xie151007',
}

s = requests.Session()

page = s.post(url_login, params=formDataLogin, verify=False)

# 【登录页】打开登录页面
formData1 = {'cases[]': '134919', 'versions[134919]': '1'}
# 【登录页】登录飞牛网
formData2 = {'cases[]': '134920', 'versions[134920]': '1'}
# 商品加入购物车
# formData3 = ''
# 【购物车】获取购物车内商品数据
formData4 = {'cases[]': '147168', 'versions[147168]': '1'}
# 【结算页】进入结算页
formData5 = {'cases[]': '136374', 'versions[136374]': '1'}
# 【结算页】订单下定
formData6 = {'cases[]': '136376', 'versions[136376]': '1'}
# 【用户中心】打开会员中心我的订单页
formData7 = {'cases[]': '147331', 'versions[147331]': '1'}
# 【用户中心】未付款订单整单退订
# formData8 = {'cases[]': '136379', 'versions[136379]': '5'}
# 【模拟支付页】使用支付宝支付
formData9 = {'cases[]': '139098', 'versions[139098]': '1'}
# 139094 【模拟支付页】打开模拟支付页
formData10 = {'cases[]': '139094', 'versions[139094]': '1'}
# 139091 【用户中心】已付款未出货订单整单退订
formData11 = {'cases[]': '139091', 'versions[139091]': '1'}
# 139090 【支付页】支付页选择支付宝点击去支付按钮
formData12 = {'cases[]': '139090', 'versions[139090]': '1'}

listData = [formData1, formData2, formData4, formData5, formData6, formData7, formData9, formData10,
            formData11, formData12]

headers2 = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
	 Chrome/51.0.2704.103 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://zentao.fn.com/index.php?m=testtask&f=linkCase&taskID=4854',
	'cookies': 'treeview=100000; pagerTesttaskLinkcase=500;lastProduct=142; windowWidth=1920;\
	 windowHeight=911; lang=zh-cn; theme=default'
}
testSuiteNumberList = [4783, 4824, 4825]
for i in range(4726, 4754):
	url_set = 'http://zentao.fn.com/index.php?m=testtask&f=linkCase&taskID=' + str(
		i) + '&param=all&moduleID=0&recTotal=&recPerPage=&orderBy=id_desc&pageID=&id='

	for item in listData:
		page2 = s.post(url_set, headers=headers2, data=item, verify=False)

print ("DONE")
