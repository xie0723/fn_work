# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/27 14:29'
import cx_Oracle


class operationDB(object):
	"""
	oracle 数据库相关操作封装
	"""

	def __init__(self):
		self.username = 'UCORDERP'
		self.password = 'q4oxh75fc1'
		self.services_host = 'dbcord01.beta1.fn'
		self.sid = 'CORD'

	# 连接数据库
	def connect_db(self):
		db = cx_Oracle.connect(self.username, self.password, self.services_host + '/' + self.sid)
		return db

	# 建立游标
	def create_cursor(self):
		cursor = self.connect_db().cursor()
		return cursor

	# 执行任意sql 语句
	def execute_sql(self, query_sql):
		result = self.create_cursor().execute(query_sql)
		return result.fetchall()

	# 根据卖场编号CM，查询成本
	def query_cost_by_CM(self, CM):
		# 根据CM查询成本sql
		query_cost_sql = "select * from ucord.show_detail where SM_SEQ = '{sm_seq}'".format(sm_seq=CM)
		return self.execute_sql(query_cost_sql)

	# 根据商品ID编号，查询成本
	def query_cost_by_CG(self, CG):
		# 根据CG查询成本sql
		query_cost_sql = "select * from ucord.show_detail where ITNO = '{ifno}'".format(ifno=CG)
		return self.execute_sql(query_cost_sql)

	# 关闭数据库连接
	def close_db(self):
		self.create_cursor().close()
		self.connect_db().close()


class getCost(object):
	def __init__(self):
		self.dbs = operationDB()

	def get_cost(self):
		pass


if __name__ == '__main__':
	# 查询商品ID为201608CG260000179的信息
	sqls = "SELECT * FROM ucord.show_detail WHERE itno ='201608CG260000179'"
	dbs = operationDB()

	# 执行sqls语句
	# print dbs.execute_sql(sqls)

	# 传入CM编号，查询
	print dbs.query_cost_by_CM('201511CM050000057')

	# 传入商品ID编号，查询
	# print dbs.query_cost_by_CG('201311CG240000159')
	# 关闭连接
	dbs.close_db()
