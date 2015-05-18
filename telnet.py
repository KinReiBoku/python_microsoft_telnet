# -*- coding: utf-8 -*-
import telnetlib

HOST = "localhost"
user = "default"
password = "password"
 
tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(user + "\r\n")
if password:
    tn.read_until("password:")
    tn.write(password + "\r\n")

tn.read_until(">")
tn.write("dir\r\n")

tn.read_until(">")
tn.write("exit\r\n")

print tn.read_all()
