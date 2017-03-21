# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/8/2 11:31'

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
import xlrd


class newTestTask(object):
	"""
	运行的时候，请先初始化4个参数，分别为登录名，登录密码，excel的表格路径，负责人的姓名。
	需要注意的时候，excel表格，默认选择第一个sheet，从第一行开始
	数据格式参考：【自营】登录-0元商品(寄销)-商品加入购物车-下定-未付款-退订
	"""

	def __init__(self, username, password, file_path, owner):
		self.username = username
		self.password = password
		self.file_path = file_path
		self.owner = owner
		try:
			self.data = xlrd.open_workbook(self.file_path)
		except IOError:
			print ('没有找到文件或打开文件失败 %s ' % self.file_path)
		self.driver = webdriver.Chrome()
		self.driver.get('http://zentao.fn.com/index.php')

	def login_zaotao(self):
		# 登录
		self.driver.find_element(By.ID, 'account').send_keys(self.username)
		self.driver.find_element(By.NAME, 'password').send_keys(self.password)
		self.driver.find_element(By.ID, 'submit').click()
		sleep(3)

	def new_test_task(self, ):
		# 点击测试频道
		self.driver.find_element(By.ID, 'menuqa').click()
		sleep(1)
		self.driver.get('http://zentao.fn.com/index.php?m=bug&f=browse&productID=142')
		# 点击测试任务
		self.driver.find_element(By.ID, 'submenutesttask').click()
		table = self.data.sheets()[0]
		for i in range(table.nrows):
			print (table.row_values(i))
			sleep(1)
			# 点击创建测试任务
			self.driver.find_element(By.CLASS_NAME, 'link-button').click()

			# 切换iframe
			self.driver.switch_to.frame('hiddenwin')

			# 点击 所属项目
			self.driver.find_element(By.ID, 'project_chzn').click()
			# 选择 所属项目 RF接口自动化测试
			self.driver.find_element(By.ID, 'project_chzn_o_1').click()
			sleep(1)

			# 点击 关联提测单
			self.driver.find_element(By.ID, 'testlist_chzn').click()
			# 选择 接口自动化测试提测单
			self.driver.find_element(By.ID, 'testlist_chzn_o_1').click()
			sleep(1)

			# 点击负责人
			self.driver.find_element(By.ID, 'owner_chzn').click()
			sleep(1)
			# 输入负责人
			self.driver.find_element(By.XPATH, ".//*[@id='owner_chzn']/div/div/input").send_keys(self.owner)
			self.driver.find_element(By.XPATH, ".//*[@id='owner_chzn']/div/div/input").send_keys(Keys.ENTER)

			# 选择开始结束日期
			self.driver.find_element(By.ID, 'begin').send_keys('2016-08-02')
			self.driver.find_element(By.ID, 'end').send_keys('2019-08-02')

			#  任务名称
			self.driver.find_element(By.ID, 'name').send_keys(table.row_values(i))

			# 保存任务
			self.driver.find_element(By.ID, 'submit').click()

			# 返还最外层
			self.driver.switch_to.default_content()
			sleep(2)

	def logout(self):
		sleep(2)
		self.driver.quit()


if __name__ == '__main__':
	zaotao = newTestTask('wangming.xie', 'Xie151007', 'd:\\test111task.xlsx', u'谢望名')
	zaotao.login_zaotao()
	zaotao.new_test_task()
	zaotao.logout()
