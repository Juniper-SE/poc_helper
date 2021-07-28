# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import re
import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Run an ansible playbook on POC devices.')
parser.add_argument('--config', nargs='*', action='store', help='send a configuration to the device in set format')
parser.add_argument('--cmd', "--command", nargs='*', action='store', help='send a configuration to the device in set format')
parser.add_argument('--output', '--out', nargs='*', action='store', metavar='filename', help='write output to a file')
parser.add_argument('hosts', choices=['all', 'nfx','qfx', 'mx', 'srx'], help='which devices to configure or command')

args = parser.parse_args()
# print(args)

# Print help message if not enough arguments supplied
if not args.config and not args.cmd:
    print("You must choose configure or command.")
    sys.exit()

# Grab all the arguments
command_config_lines = sys.argv[2]
hosts = args.hosts
filename = ''
lines = ''

if args.config:
    filename = 'config.yml'
    line1 = "        lines:\n"

    for val in args.config[0].split("\n"):
        lines += "          - " + val + "\n"

    # Replace the hosts in ansible file with supplied one
    with open(filename, 'r') as ansible:
        data = ansible.readlines()
        data[2] = "  hosts: " + hosts + "\n"
        data[14] = line1
        data[15:] = lines

    with open(filename, 'w') as write_file:
        write_file.writelines(data)
elif args.cmd:
    filename = 'command.yml'
    lines = "commands:\n"

    for val in args.cmd[0].split("\n"):
        lines += "          - " + val + "\n"
    lines += "      "

    # Replace the hosts in ansible file with supplied one
    with open(filename, 'r') as ansible:
        data = ansible.read()
        data = re.sub(r'hosts:.+', "hosts: " + hosts, data)
        data = re.sub(r'commands:(.|\s)+?(?=register)', lines, data)

    with open(filename, 'w') as write_file:
        write_file.writelines(data)

ansible_command = "ansible-playbook " + filename + " -i inventory"
print(ansible_command)

if args.output:
    logfile = open(args.output[0], 'w+')
    proc = subprocess.Popen(ansible_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        sys.stdout.write(line.decode('utf-8'))
        logfile.write(line.decode('utf-8'))
    proc.wait()
else:
    proc = subprocess.Popen(ansible_command)
    proc.wait()
# os.system(ansible_command)
