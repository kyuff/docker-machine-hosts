#!/usr/bin/python

import subprocess
import re

hosts = "hosts"

def run(command):
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
    return iter(pipe.stdout.readline, b"")


def list_vms():
    vms = []
    for line in run(["VBoxManage", "list", "runningvms"]):
        m = re.search('\"([^"]*)\"', line)
        vms.append(m.group(1))
    return vms

def get_ip(vm):
    for line in run(["VBoxManage", "guestproperty", "get", vm, "/VirtualBox/GuestInfo/Net/1/V4/IP"]):
        m = re.search("Value:\s*([0-9\.]*)", line)
        return m.group(1)

file = open(hosts)

buffer = ""

for line in file.readlines():
    m = re.search("^#\sDOCKER\sHOSTS", line)
    if re.match("^#\sDOCKER\sHOSTS", line):
        break
    else:
        buffer += line
file.close()

buffer += "# DOCKER HOSTS\n"

for vm in list_vms():
    ip = get_ip(vm)
    buffer += "{0}\t{1}.local\n".format(ip, vm)

file = open(hosts, "w")
file.write(buffer)
file.close()
