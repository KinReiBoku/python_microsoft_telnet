# -*- coding: utf-8 -*-
from pexpect import spawn

# 接続情報
HOST = '192.168.43.50'
USER = 'default'
PASS = 'password'
PORT = 23
LINUX_SIGN =  ('# ', '$ ')
WINDOWS_SIGN = '>'

class telnet_host(object):

	# 初期化
	def __init__(self, user, addr, passwd, port):
		self.m_user = user
		self.m_addr = addr
		self.m_pass = passwd
		self.m_port = port
		self.m_conn = None

	# 接続
	def telnet_connect(self):
		c = spawn('sh')
		c.expect([LINUX_SIGN[0], LINUX_SIGN[1]])
		c.sendline('export TERM=vt100')
		c.expect([LINUX_SIGN[0], LINUX_SIGN[1]])
		c.sendline('telnet -l %s %s %s' % (self.m_user, self.m_addr, self.m_port))
		c.expect('[Pp]assword:')
		c.send(self.m_pass + '\r')
		c.expect(WINDOWS_SIGN)
		self.m_conn = c
		return c

	# 切断
	def telnet_disconnect(self):
		if self.m_conn is None:
			return
		c = self.m_conn
		c.send('exit\r')
		c.expect_exact([LINUX_SIGN[0], LINUX_SIGN[1]])
		c.close()
		self.m_conn = None
		return

if __name__ == '__main__':

	telnet = telnet_host(
		USER,
		HOST,
		PASS,
		PORT
	)
	c = telnet.telnet_connect()
	print "telnet login ok"

	telnet.telnet_disconnect()
	print "telnet logout ok"
