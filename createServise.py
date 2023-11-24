import os
import subprocess
from sys import argv

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# temp, nameDir= argv# nameMain = argv
# print(nameDir)
nameMainFile = input('Название исполняемого файла: ')
# nameMainFile = "test2.py"

cmd = "pwd" 
returned_output = subprocess.check_output(cmd)
pwd = returned_output.decode("utf-8").replace('\n', '')
nameDir = pwd.split('/')[-1]

cmd = 'whoami'
returned_output = subprocess.check_output(cmd)
userName = returned_output.decode("utf-8")

pwd = f'{pwd}'
nameServiceFile =  f'{nameDir}.service' 

with open(pwd +'/'+ nameServiceFile,'w') as file:
    file.write(f"""
[Unit]
Description= nameMain Bot
After=network.target

[Service]
User={userName}
Group=user

WorkingDirectory={pwd}
Environment="PYTHONPATH={pwd}"
ExecStart=python3 {pwd}/{nameMainFile}

# Restart=on-failure
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
a
# sudo cp {pwd}/{nameServiceFile} /etc/systemd/system/{nameServiceFile}
"""
)
    file.close()
    

cmd = "pwd" 
returned_output = subprocess.check_output(cmd)
pwd = returned_output.decode("utf-8")

print(bcolors.OKGREEN + f'[+] Сервисный файл создан по пути -> {pwd}' + bcolors.ENDC)

