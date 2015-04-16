import os
import telnetlib

HOST = "localhost"
USER = "default"
PASS = "password"

class telnet_host:

	def __init__(self, host="localhost", port=23):
		self.host = host
		self.port = port
		self.conn = None
		print host
		print port

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
		self.conn.get_socket().send("Clear-Host\r\n")
		self.conn.read_until('>')
		self.conn.get_socket().send(buf)
		self.conn.read_until(sign)
		self.conn.get_socket().send("echo $?\r\n")
		result = self.conn.expect(["True", "False"])
		result1 = result[2].decode('cp932').encode('utf-8')
		r = re.compile(r'\x1b\[.*?m\[?')
		result2 = re.sub(r,'',result1)
		return [result[0], result2]

	def read(self, buf):
		self.conn.read_until(buf)

	def set_option(self, sock, cmd, opt):
		if opt == telnetlib.TTYPE and cmd in (telnetlib.DO):
			sock.sendall(telnetlib.IAC + telnetlib.WILL + telnetlib.TTYPE)
			sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TTYPE + chr(0) +  'vt100' + telnetlib.IAC  + telnetlib.SE)
		elif opt != telnetlib.NOOPT:
			if cmd in (telnetlib.DO, telnetlib.DONT):
				sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
			elif cmd in (telnetlib.WILL, telnetlib.WONT):
				sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

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
