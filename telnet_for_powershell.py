import os
import telnetlib
 
HOST = "192.168.43.40"
USER = "default"
PASS = "password"

class telnet_host:

	def __init__(self, host="localhost", port=23):
		self.host = host
		self.port = port
		self.conn = None

	def open(self, user, password):
		self.conn = telnetlib.Telnet(self.host, self.port)
		self.conn.set_option_negotiation_callback(self.set_option)
		self.conn.read_until("login: ")
		self.conn.write(user + "\r\n")
		if password:
			self.conn.read_until("password:")
			self.conn.write(password + "\r\n")
		self.conn.read_until('>')

	def close(self):
		self.conn.close()

	def write(self, buf, sign):
		self.conn.get_socket().send(buf)
		self.conn.read_until(sign)

	def read(self, buf):
		self.conn.read_until(buf)

	def set_option(self, sock, cmd, opt):
		if opt == telnetlib.TTYPE and cmd in (telnetlib.DO):
			self.sock.sendall(telnetlib.IAC + telnetlib.WILL + telnetlib.TTYPE)
		elif opt == telnetlib.TTYPE and cmd in (telnetlib.SB):
			self.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TTYPE + chr(0) +  'vt100' + telnetlib.IAC  + telnetlib.SE)

if __name__ == '__main__':

	telnet = telnet_host(HOST)
	telnet.open(USER, PASS)
	print "telnet login ok"

	telnet.write("powershell\r\n", '>')
	print "powershell start ok"

	telnet.write("exit\r\n", '>')
	print "powershell stop ok"

	telnet.close()
	print "telnet logout ok"
