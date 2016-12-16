# -*- coding: utf-8 -*-
import time

__Author__ = "xiewm"
__Date__ = '2016/11/8 17:11'

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


class fnWeekTask(object):
	def __init__(self):
		self.driver = webdriver.Chrome()
		# self.driver = webdriver.PhantomJS()

	# 打开首页
	def open_home_page(self):
		self.driver.get('http://zentao.fn.com/index.php')
		return self

	# 登录
	def login_fn(self):
		self.driver.find_element(By.ID, 'account').send_keys('wangming.xie')
		self.driver.find_element(By.NAME, 'password').send_keys('Xie151008')
		self.driver.find_element(By.ID, 'submit').click()
		return self

	# 跳转到测试部日常工作page
	def jump_to_work_page(self):
		self.driver.get('http://zentao.fn.com/index.php?m=project&f=task&projectID=967&type=all')
		return self

	# 点击建任务
	def click_new_task(self):
		self.driver.find_element(By.XPATH, '//*[@id="featurebar"]/div[2]/span[5]').click()
		return self

	# 更改dispaly 属性
	def exe_js(self):
		js = "document.getElementById('module').style='dispaly:1;'"
		self.driver.execute_script(js)
		return self

	# 选择所属模块
	def select_moudle(self):
		Select(self.driver.find_element(By.ID, 'module')).select_by_value('10707')
		return self

	# 选择指派给谁
	def select_to_name(self):
		js = "document.getElementById('assignedTo').style='dispaly:1;'"
		self.driver.execute_script(js)
		Select(self.driver.find_element(By.ID, 'assignedTo')).select_by_value('wangming.xie')
		return self

	# 选择任务类型
	def select_task_type(self):
		Select(self.driver.find_element(By.ID, 'type')).select_by_value('test')
		return self

	# 输入任务名称
	def input_task_name(self):
		self.driver.find_element(By.ID, 'name').send_keys(u'每周测试任务')
		return self

	# 输入最初预计时间
	def input_excepte_time(self):
		self.driver.find_element(By.ID, 'estimate').send_keys('40')
		return self

	# 输入预计开始时间
	def input_except_start_time(self):
		self.driver.find_element(By.ID, 'estStarted').send_keys('2016-11-28')
		return self

	# 输入截止日期
	def input_except_end_time(self):
		self.driver.find_element(By.ID, 'deadline').send_keys('2016-12-2')
		return self

	# 保存
	def save_(self):
		self.driver.maximize_window()
		self.driver.find_element(By.ID, 'submit').click()
		time.sleep(5)
		return self

	# 退出
	def quit_driver(self):
		self.driver.quit()

	def run_(self):
		self.open_home_page().login_fn().jump_to_work_page().click_new_task().exe_js().select_moudle(). \
			select_to_name().select_task_type().input_task_name().input_excepte_time().input_except_start_time(). \
			input_except_end_time().save_().quit_driver()

	# 获取当前时间
	@staticmethod
	def get_now_time():
		print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		return time.strftime("%Y-%m-%d", time.localtime())

if __name__ == '__main__':
	fnwork = fnWeekTask()
	fnwork.run_()
