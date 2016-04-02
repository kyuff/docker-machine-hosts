#!/usr/bin/python

import re
import subprocess

hosts = "/etc/hosts"
tmp = "/tmp/hosts"


def run(command):
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
    return iter(pipe.stdout.readline, b"")


def list_new_entries():
    entries = []
    for line in run(["docker-machine", "ls", "-f", r'{{.Name}}#{{.URL}}']):
        m = re.search('^([^#]*)#[^:]*://([^:]*):\d*$', line)
        name = m.group(1)
        ip = m.group(2)
        entries.append("{0}\t{1}.local\n".format(ip, name))
    return entries


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

for entry in list_new_entries():
    buffer += entry

file = open(tmp, "w")
file.write(buffer)
file.close()

print "Writing the following /etc/hosts:"
print buffer
for line in run(["cp", hosts, "{0}.bak".format(tmp)]):
    print line

for line in run(["sudo", "mv", tmp, hosts]):
    print line
