# -*- coding: utf-8 -*-
import os
import re
import telnetlib

HOST = "localhost"
USER = "default"
PASS = "password"

WIN_SIGN = WIN_SIGN

class telnet_host:

	def __init__(self, host="localhost", port=23):
		self.host = host
		self.port = port
		self.conn = None

	def open(self, user, password):
		# Telnet接続
		self.conn = telnetlib.Telnet(self.host, self.port)
		self.conn.set_option_negotiation_callback(self.set_option)
		# ユーザ名入力
		self.conn.read_until("login: ")
		self.conn.write(user + "\r\n")
		# パスワード入力
		if password:
			self.conn.read_until("password:")
			self.conn.write(password + "\r\n")
		self.conn.read_until(WIN_SIGN)
		# 表示言語を英語に変更
		self.conn.write("chcp 437\r\n")
		self.conn.read_until(WIN_SIGN)

	def close(self):
		# Telnet切断
		self.conn.close()

	def write(self, buf, sign):
		# 画面クリア
		self.conn.get_socket().send("Clear-Host\r\n")
		self.conn.read_until(WIN_SIGN)
		# コマンド実行
		self.conn.get_socket().send(buf)
		result = self.conn.read_until(sign)
		# コマンド実行結果の取得
		command = "echo $?"
		self.conn.get_socket().send(command + "\r\n")
		buf = self.conn.expect(["True", "False"])
		result += buf[2]
		# 実行コマンドの除去
		result = re.sub(r'\x1b\[.*?[A-Z]', '', result)
			for cmd in [buf, command]:
				esp_tuple = ("\\", ".", "^", "$", "*", "+", "?", "{", "[", "]", "|", "(", ")")
				for esp in esp_tuple:
				if esp == "\\":
					cmd = re.sub('\\'+esp,'\\\\\\'+esp,cmd)
				else:
					cmd = re.sub('\\'+esp,'\\'+esp,cmd)
				result = re.sub(cmd, '', result)
			# プロンプトの除去
			result = re.sub(r'PS .*>', '', result)
			# echo $?実行結果の除去
			result = result.strip('True')
			result = result.strip('False')
			# 前後の空白文字の除去
			result = result.lstrip()
			result = result.rstrip()
		return [buf[0], result]

	def read(self, buf):
		self.conn.read_until(buf)

	def set_option(self, sock, cmd, opt):
		# TerminalTypeを聞かれたらvt100を返却する
		if opt == telnetlib.TTYPE and cmd in (telnetlib.DO):
			sock.sendall(telnetlib.IAC + telnetlib.WILL + telnetlib.TTYPE)
			sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TTYPE + chr(0) + 'vt100' + telnetlib.IAC + telnetlib.SE)
		# それ以外は拒否する
		elif opt != telnetlib.NOOPT:
			if cmd in (telnetlib.DO, telnetlib.DONT):
				sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
			elif cmd in (telnetlib.WILL, telnetlib.WONT):
				sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

if __name__ == '__main__':

	telnet = telnet_host(HOST)
	telnet.open(USER, PASS)
	print "telnet login ok"

	telnet.write("powershell\r\n", WIN_SIGN)
	print "powershell start ok"

	telnet.write("exit\r\n", WIN_SIGN)
	print "powershell stop ok"

	telnet.close()
	print "telnet logout ok"
