# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/9/23 8:20'

import requests


class Zentao(object):
	def __init__(self):
		self.login_url = 'http://zentao.fn.com/index.php?m=user&f=login'
		self.referer_url = 'http://zentao.fn.com/index.php?m=project&f=task&projectID=967'
		self.account = 'wangming.xie'
		self.password = 'Xie151008'
		self.session.headers  = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
						(KHTML, like Gecko)Chrome/51.0.2704.103 Safari/537.36',
		}
		self.session = requests.Session()
		self.session.verify = False 
		self.create_tasks_url = 'http://zentao.fn.com/index.php?m=task&f=create&project=967'

	def login_zt(self):
		data = {
			'account': self.account,
			'password': self.password,
			'referer': self.referer_url
		}

		resp = self.session.post(url=self.login_url, data=data)
		print (resp.text)

	def create_tasks(self):
		content_disposition = {
							'Content-Disposition: form-data; name="after"':'toTaskList',
							'Content-Disposition: form-data; name="assignedTo[]"':'wangming.xie',
							'Content-Disposition: form-data; name="deadline"':'2016-09-23',
							'Content-Disposition: form-data; name="desc"':'<div>&nbsp;客服三期测试&nbsp;</div>',
							'Content-Disposition: form-data; name="estimate"':40,
							'Content-Disposition: form-data; name="estStarted"':'2016-09-19',
							'Content-Disposition: form-data; name="files[]"':' ',
							'Content-Disposition: form-data; name="files[]"':' ',
							'Content-Disposition: form-data; name="labels[]"':' ',
							'Content-Disposition: form-data; name="labels[]"':' ',
							'Content-Disposition: form-data; name="mailto[]"':' ',
							'Content-Disposition: form-data; name="module"':0,
							'Content-Disposition: form-data; name="name"':'客服三期测试',
							'Content-Disposition: form-data; name="pri"':1,
							'Content-Disposition: form-data; name="type"':'test',
							}
		self.session.get('http://zentao.fn.com/index.php?m=task&f=create&project=967')
		self.session.get('http://zentao.fn.com/index.php?m=story&f=ajaxGetProjectStories&t=html&projectID=967&productID=0&moduleID=10707')
		resp = self.session.post(url=self.create_tasks_url,data=content_disposition)
		self.session.get('http://zentao.fn.com/index.php?m=project&f=browse&projectID=967&tab=task',allow_redirects=True)
		self.session.get('http://zentao.fn.com/index.php?m=project&f=task&projectID=967')
		print (resp.json())


if __name__ == '__main__':
	lnzt = Zentao()
	lnzt.login_zt()
	lnzt.create_tasks()


