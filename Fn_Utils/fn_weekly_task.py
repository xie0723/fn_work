# -*- coding: utf-8 -*-
import time

__Author__ = "xiewm"
__Date__ = '2016/11/8 17:11'

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('http://zentao.fn.com/index.php')
# 登录
driver.find_element(By.ID, 'account').send_keys('wangming.xie')
driver.find_element(By.NAME, 'password').send_keys('Xie151008')
driver.find_element(By.ID, 'submit').click()

# 跳转到测试部日常工作page
driver.get('http://zentao.fn.com/index.php?m=project&f=task&projectID=967&type=all')
# 点击建任务
driver.find_element(By.XPATH, '//*[@id="featurebar"]/div[2]/span[5]').click()

# 更改dispaly 属性
js = "document.getElementById('module').style='dispaly:1;'"
driver.execute_script(js)

# 选择所属模块
Select(driver.find_element(By.ID, 'module')).select_by_value('10707')

# 选择指派给
js = "document.getElementById('assignedTo').style='dispaly:1;'"
driver.execute_script(js)
Select(driver.find_element(By.ID, 'assignedTo')).select_by_value('wangming.xie')

# 选择任务类型
Select(driver.find_element(By.ID, 'type')).select_by_value('test')

# 输入任务名称
driver.find_element(By.ID, 'name').send_keys(u'每周测试任务')

# 输入最初预计时间
driver.find_element(By.ID, 'estimate').send_keys('40')

# 输入预计开始时间
driver.find_element(By.ID, 'estStarted').send_keys('2016-11-07')

# 输入截止日期
driver.find_element(By.ID, 'deadline').send_keys('2016-11-11')

# 保存
driver.maximize_window()
driver.find_element(By.ID, 'submit').click()

time.sleep(5)
driver.quit()


def get_now_time():
	print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	return time.strftime("%Y-%m-%d", time.localtime())
