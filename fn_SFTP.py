# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2016/8/26 16:38'

"""
主机：211.95.120.6
端口：54321
协议：SFTP-SSH File Transfer Protocol
用户：feiniutest
密码：feiniutest

"""
import os
import paramiko
import datetime


class SFTP(object):
	def __init__(self, obj):
		self.obj = obj

	# 绑定到目标，一般是as后的对象
	def __enter__(self, obj):
		return self.obj

	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			self.obj.close()
		except AttributeError:
			print ('Not closeable.')
			return True


class fnSFTP(object):
	def __init__(self):
		self.host = "211.95.120.6"
		self.port = 54321
		self.user = "feiniutest"
		self.password = "feiniutest"
		# 默认本地目录
		self.local_path = 'd:/coding/fn_work/'
		# 默认服务器目录
		self.server_path = '/home/ecommerence/feiniutest/snd/test/'

	# 登录sftp 服务器
	def login_fn_sftp(self):
		try:
			t = paramiko.Transport((self.host, self.port))
			t.connect(username=self.user, password=self.password)
			sftp = paramiko.SFTPClient.from_transport(t)
		except Exception as e:
			print (e)
			print ('登录失败')
		return sftp
		t.close()

	# 上传文件
	def fn_upload_file(self, local_file, server_file):
		try:
			server_file = self.server_path + server_file
			local_file = self.local_path + local_file
			sftp = self.login_fn_sftp()
			sftp.put(local_file, server_file)
			print ("upload file success :%s" % local_file)
		except Exception as e:
			print (e)
			print ('文件上传失败')
		finally:
			sftp.close()

	# 下载单个文件
	def fn_down_file(self, server_file, local_file):
		try:
			server_file = self.server_path + server_file
			local_file = self.local_path + local_file
			sftp = self.login_fn_sftp()
			sftp.get(server_file, local_file)
			print ("down file success :%s " % server_file)
		except Exception as e:
			print (e)
			print ('文件下载失败')
		finally:
			sftp.close()

	# 批量下载文件
	def fn_batch_down_file(self, remote_dir='/home/ecommerence/feiniutest/snd/test/', local_dir=None):
		try:
			sftp = self.login_fn_sftp()
			files = sftp.listdir(remote_dir)
			for f in files:
				print ('Downloading file:%s  %s ' % (os.path.join(remote_dir, f), datetime.datetime.now()))
				sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))  # 批量下载
				print ('Download file success :%s ' % datetime.datetime.now())
		except Exception as e:
			print (e)
			print ("批量下载失败")
		finally:
			sftp.close()

	# 执行linux 命令
	def fn_exec_command(self, command):
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.host, self.port, self.user, self.password)
			std_in, std_out, std_err = ssh_client.exec_command(command)
			for line in std_out:
				print (line.strip("\n"))
			ssh_client.close()
		except Exception as e:
			print (e)
			print ('linux命令执行错误')


if __name__ == '__main__':
	fn_sftp = fnSFTP()
	# fn_sftp.login_fn_sftp()
	# 下载
	fn_sftp.fn_down_file('1.txt', '1.txt')
	# 上传
	# fn_sftp.fn_upload_file('xwm_test111.txt', 'xwm_test111.txt')
	# 批量下载
	# fn_sftp.fn_batch_down_file('/home/ecommerence/feiniutest/snd/test/','d:/coding/fn_work/')
	# fn_sftp.fn_batch_down_file()
