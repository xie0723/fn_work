# -*- coding: utf-8 -*-
import time

import xlrd

from selenium.webdriver.common.by import By

__Author__ = "xiewm"
__Date__ = '2016/8/5 18:09'

from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://zentao.fn.com/index.php')
# 登录
driver.find_element(By.ID, 'account').send_keys('wangming.xie')
driver.find_element(By.NAME, 'password').send_keys('Xie151007')
driver.find_element(By.ID, 'submit').click()

# 点击测试频道
time.sleep(3)
driver.find_element(By.ID, 'menuqa').click()
# 点击用例库
time.sleep(3)
driver.get('http://zentao.fn.com/index.php?m=testcase&f=browse&productID=142')


data = xlrd.open_workbook('D:\\automation.xlsx')
table = data.sheets()[0]
for i in range(table.nrows):
	print (table.row_values(i))
	# 点击建用例
	time.sleep(1)
	driver.find_element(By.XPATH, ".//*[@id='featurebar']/div[2]/span[4]/a").click()

	# 选择使用阶段-功能测试
	time.sleep(1)
	driver.find_element(By.XPATH, '//*[@id="stage"]/option[3]').click()

	# 点击相关需求
	time.sleep(2)
	driver.find_element(By.ID, 'story_chzn').click()
	time.sleep(1)

	# 选择第一个需求
	driver.find_element(By.ID, 'story_chzn_o_1').click()

	# 输入用例标题

	driver.find_element(By.ID, 'title').send_keys(table.row_values(i))

	time.sleep(1)
	# js = "var q=document.documentElement.scrollTop=100000"
	# driver.execute_script(js)

	#  js 实现点击保存
	time.sleep(2)
	js_click = "document.getElementById('submit').click()"
	driver.execute_script(js_click)

time.sleep(1)
driver.quit()
