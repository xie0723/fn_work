# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/10/27 14:29'
import cx_Oracle
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


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
		try:
			db = cx_Oracle.connect(self.username, self.password, self.services_host + '/' + self.sid)
			return db
		except Exception as e:
			print u'服务器连接失败，请检查设置', e

	# 建立游标
	def create_cursor(self):
		cursor = self.connect_db().cursor()
		return cursor

	# 执行任意sql
	def execute_sql(self, query_sql):
		result = self.create_cursor().execute(query_sql)
		return result.fetchall()

	# 通过订单编号，从order_group表中查询对应的QG_SEQ
	def get_qg_seq(self, CP):
		query_qg_seq_sql = "SELECT ORDER_GROUP.OG_SEQ FROM UCORD.ORDER_GROUP WHERE OG_NO = '{OG_NO}'".format(OG_NO=CP)
		return self.execute_sql(query_qg_seq_sql)

	# 通过QG_SEQ，从order_list 表中查询订单的所有信息
	def query_info_by_qg_seq(self, qg_seq):
		query_info_sql = "SELECT * FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_info_sql)

	# 通过qg_seq，从order_list 表中查询订单中商品的成本
	def query_cost(self, qg_seq):
		query_cost_sql = "SELECT COST FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_cost_sql)

	# 通过qg_seq，从order_list 表中查询订单中商品的类型
	def query_kind(self, qg_seq):
		query_kind_sql = "SELECT KIND FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_kind_sql)

	# 通过qg_seq，从order_list 表中查询订单中商品（子商品）的名称
	def query_it_name(self, qg_seq):
		query_it_name_sql = "SELECT ITNAME FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_it_name_sql)

	# 通过qg_seq，从order_list 表中查询订单中商品的卖场名称
	def query_sell_name(self, qg_seq):
		query_sell_name_sql = "SELECT SELL_NAME FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_sell_name_sql)

	# 通过qg_seq，从order_list 表中查询订单中商品的卖场编号CM
	def query_sell_no(self, qg_seq):
		query_sell_no_sql = "SELECT SELL_NO FROM UCORD.ORDER_LIST WHERE OG_SEQ = \'{QG_SEQ}\'". \
			format(QG_SEQ=qg_seq[0][0])
		return self.execute_sql(query_sell_no_sql)

	# 关闭数据库连接
	def close_db(self):
		self.create_cursor().close()
		self.connect_db().close()


class analyseData(operationDB):
	def __init__(self):
		super(analyseData, self).__init__()
		self._test_datas = {
			('201511CM110000033', 2): u'进销单品',
			('201607CM260000016', 112.5): u'寄销单品',
			('201511CM050000190', 0): u'门店单品',
			('201511CM050000057', 95): u'转单单品',
			('201511CM110000039', 2): u'预购商品',
			('201511CM120000010', 33.75): u'单品多件',
			('201511CM120000014', 44.26): u'特卖变价',
			('201511CM110000038', 8): u'主+配+赠+加',
			('201511CM050000195', 0): u'组合商品',
			('201511CM120000011', 25.43): u'优惠套餐0',
			('201511CM110000027', 34.58): u'优惠套餐1',
			('201608CM150000043', 54.01): u'组合商品+加',
		}

	def test_new_assert(self, CP):
		QG_SEQ = self.get_qg_seq(CP)
		costs = [_[0] for _ in self.query_cost(QG_SEQ)]
		sell_nos = [_[0] for _ in self.query_sell_no(QG_SEQ)]
		temp = {}
		for sno, c in zip(sell_nos, costs):
			if sno not in temp:
				temp[sno] = c
			else:
				temp[sno] = temp.get(sno) + c
		for _ in temp.items():
			if _ in self._test_datas.keys():
				print '{0} ,{1} == {2}  √'.format(self._test_datas[_], _[1], _[1])
			else:
				print self._test_datas[_], '错误值：%s' % _[1], '正确值：%s' % _[0]

			# 获取订单的总成本

	def show_total_cost(self, CP):
		QG_SEQ = self.get_qg_seq(CP)
		total_cost = reduce(lambda x, y: x + y, [item[0] for item in self.query_cost(QG_SEQ)])
		print_msg = u'订单：%s 的总成本是→' % CP + str(total_cost)
		print print_msg
		return total_cost

	# 获取整比订单内商品的成本（包括组合类型商品的子商品成本）
	def show_all_cost(self, CP):
		QG_SEQ = self.get_qg_seq(CP)
		costs = [_[0] for _ in self.query_cost(QG_SEQ)]
		sell_names = [_[0] for _ in self.query_sell_name(QG_SEQ)]
		for c, sn in zip(costs, sell_names):
			print sn, c

	# 输出单商品类型的名称 和成本
	def show_single_cost_detail(self, CP):
		QG_SEQ = self.get_qg_seq(CP)
		kinds = self.query_kind(QG_SEQ)
		costs = self.query_cost(QG_SEQ)
		sell_names = self.query_sell_name(QG_SEQ)

		for k, c, sn in zip(kinds, costs, sell_names):
			if int(k[0]) == 1:
				print sn[0] + '：→' + '(' + str(c[0]) + ')'

	# 输出组合类型商品的名称 和成本
	def show_group_cost_detail(self, CP):
		QG_SEQ = self.get_qg_seq(CP)
		kinds = [_[0] for _ in self.query_kind(QG_SEQ)]
		costs = [_[0] for _ in self.query_cost(QG_SEQ)]
		sell_names = [_[0] for _ in self.query_sell_name(QG_SEQ)]
		sell_nos = [_[0] for _ in self.query_sell_no(QG_SEQ)]

		# 筛选出全部是组合类型的商品，存在group_type
		group_type = []
		for k, sn, sno, c in zip(kinds, sell_names, sell_nos, costs):
			if k != '1' and kinds.count(k) > 1 or sell_nos.count(sno) > 1:
				group_type.append((k, sn, sno, c))

		# 筛选全部为优惠套餐类型的商品，存在Discount_type
		discount_type = [(_[1], _[-1]) for _ in group_type if _[0] == '13']
		discount_cost = str(reduce(lambda x, y: x + y, [_[-1] for _ in discount_type]))
		print u'{0}的总成本是：{1}'.format(discount_type[0][0], discount_cost)
		print u'优惠套餐内子商品成本分别是：'
		for i in discount_type:
			print '{0}→{1}'.format(i[0], i[1])
		print '--------------------------------------------------------------'
		group_type_ = [item for item in group_type if item[0] != '13']
		group_dict = {}
		for i in group_type_:
			if i[1] not in group_dict:
				group_dict[i[1].strip()] = i[-1]
			else:
				new_cost = group_dict.get(i[1].strip()) + i[-1]
				group_dict[i[1].strip()] = new_cost
		for k in group_dict:
			print u'{0}的总成本是：{1}'.format(k, group_dict[k])

	# 校验指定订单的成本
	def should_be_cost_equal(self, cost, CP):
		print u'==========================单商品类型=========================='
		self.show_single_cost_detail(CP)
		print u'==========================组合商品类型========================'
		self.show_group_cost_detail(CP)
		if cost == self.get_total_cost(CP):
			print u'订单成本校验成功'
		else:
			print u'成本计算错误'


if __name__ == '__main__':
	# 通过订单编号，查询订单中商品信息
	# sqls = "SELECT * FROM UCORD.ORDER_LIST WHERE OG_SEQ = (SELECT ORDER_GROUP.OG_SEQ FROM UCORD.ORDER_GROUP \
	# 		WHERE OG_NO = '201611CP03091636')"
	# dbs = operationDB()

	# 执行sqls语句
	# print dbs.execute_sql(sqls)

	# 传入订单CP编号查询qg_seq
	# qg_seqs = dbs.get_qg_seq('201611CP03091675')

	# print dbs.query_cost(qg_seq)
	# print dbs.query_it_name(qg_seq)
	# 传入商品ID编号，查询
	# print dbs.query_cost_by_CG('201311CG240000159')
	# 关闭连接
	# dbs.close_db()
	# ------------------------------------------------------------------------------------------
	datas = analyseData()
	# qg_seqs = datas.get_qg_seq('201611CP03091675')
	# datas.get_total_cost('201611CP03091751')
	# datas.show_single_cost_detail('201611CP03091796')
	# datas.show_group_cost_detail('201611CP03091796')
	datas.test_new_assert('201611CP03091796')
	# datas.show_all_cost('201611CP03091796')
	# print datas.query_kind(qg_seqs)
	# print datas.query_cost(qg_seqs)
	datas.close_db()
