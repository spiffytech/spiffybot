import os
import platform
import re

system = platform.system()

def getIP(interface):
    ifconfig = os.popen("/sbin/ifconfig").read().split("\n")
    found = 0
    for line in range(0, len(ifconfig)):
        if ifconfig[line].find(interface) != -1:
            found = 1
            break
    if found == 0:
        return "no such interface"
        print "args =", args
    else:
        ip = re.findall("addr:\d+.\d+.\d+.\d+", ifconfig[line+1])
        if len(ip) != 0:
            return ip[0].partition(":")[2]
        else:
            return "No IP on that interface" 

def getLoad():
    uptime = os.popen("uptime").read()
    return " ".join(uptime.split(" ")[11:])

def whoIs():
    return "".join(system, platform.release())
