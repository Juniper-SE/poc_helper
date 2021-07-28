#!/usr/bin/env python3

# This script (called PocHelper) has two modes. It either takes a list of Junoss set commands and applies them to a
# Junos device or group of devices found in the Ansible 'inventory' file. Or, it runs a single command on a device/group.
# It can save the output of the run, though this is only useful for commands.
#
# Erik Sherk & Natalie Landsberg 4/6/21

import sys
import re
import os
import argparse
import subprocess
from jinja2 import Template

# Function: Look to see if the host(s) from the cmd line is in the 'inventory' file
def inventory(hosts):
    for i, line in enumerate(open('inventory','r')):
#        print(line)
        if hosts in line:
            return True
    return False

parser = argparse.ArgumentParser(description='Run an ansible playbook on POC devices.')
parser.add_argument('--config', action='store', help='send a configuration to the device in set format')
#parser.add_argument('--cmd', "--command", nargs='*', action='store', help='send a configuration to the device in set format')
parser.add_argument('--cmd', "--command", action='store', help='send a configuration to the device in set format')
parser.add_argument('-o', '--out', action='store', metavar='filename', help='write output to a file')
parser.add_argument('hosts', help='which devices to configure or command')

args = parser.parse_args()
print(args)

if (not inventory(args.hosts)):
    print("{} is not in the inventory file!".format(args.hosts))
    sys.exit()
    
# Print help message if not enough arguments supplied
if not args.config and not args.cmd:
    print("You must choose configure or command.")
    sys.exit()

hosts = args.hosts
filename = 'out.yml'
lines = ''

if args.config:
    for val in args.config.split("\n"):        
        lines += "          - " + val +"\n"
    print("Lines: ", lines)

    teml ='''---
- name: Run the command or configuration on devices
  hosts: {{hosts}}
  roles:
    - Juniper.junos
  gather_facts: no
  connection: local

  tasks:
    - name: Configure Juniper device
      juniper_junos_config:
        provider:
          host: "{% raw %}{{ ansible_host }}{% endraw %}"
          user: "jnpr"
        comment: Brought to you by PocHelper
        load: set
        lines:
{{lines}}
'''

# Config
elif args.cmd:
    for val in args.cmd[0].split("\n"):
        lines += "- " + val
    
    teml ='''---
- name: Run the command or configuration on devices
  hosts: {{hosts}}
  roles:
    - Juniper.junos
  gather_facts: no
  connection: local

  tasks:
    - name: Configure Juniper device
      juniper_junos_config:
        provider:
          host: "{% raw %}{{ ansible_host }}{% endraw %}"
          user: "jnpr"
        commands:
          {{lines}}
      register: junos_result

    - name: Print response
      debug:
        var: junos_result.stdout_lines
'''

# End cmd

tp = Template(teml)
yml = tp.render(hosts=hosts, lines=lines)

# Write our teemplate to out.yml
with open(filename, 'w') as write_file:
    write_file.writelines(yml)

print(yml)

ansible_command = "ansible-playbook " + filename + " -i inventory"
print(ansible_command)

print("args.out: ", args.out)
if args.out:
    logfile = open(args.out, 'w+')    
    proc = subprocess.Popen(ansible_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        sys.stdout.write(line.decode('utf-8'))
        logfile.write(line.decode('utf-8'))
    proc.wait()
else:
    proc = subprocess.Popen(ansible_command.split())
    proc.wait()

sys.exit()

        
