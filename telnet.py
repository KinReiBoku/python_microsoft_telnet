import telnetlib
import time
 
HOST = "192.168.10.40"  # your server
user = "default"             # your username
password = "password"       # your password
 
tn = telnetlib.Telnet(HOST)
 
tn.read_until("login: ")
tn.write(user + "\r\n")
if password:
    tn.read_until("password:")
    tn.write(password + "\r\n")

#tn.write(user.encode('ascii') + "\r\n".encode('ascii'))
#res = tn.write("dir\r\n")
#print tn.read_all()

tn.write("powershell\r\n")

time.sleep(120)
tn.write("$Server = Connect-VIServer -Server 192.168.10.30 -User root -Password vmware\r\n")

time.sleep(120)
tn.write("Get-VDSwitch -Name VDSwitch | New-VDPortgroup -Name VDPortGroup2 -VlanId 10\r\n")
