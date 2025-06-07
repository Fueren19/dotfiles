#!/bin/python
import subprocess, sys
option = str(sys.argv[1])
options = ["Yeniden", "Bilgisayarı", "Oturumu", "Uyku"]
commands = {"Yeniden": ["reboot"], "Bilgisayarı": ["systemctl", "poweroff"],
            "Uyku": ["systemctl", "suspend"], "Oturumu": ["hyprctl", "dispatch", "exit"]}
for i in options:
    if i == option:
        subprocess.run(commands[i])