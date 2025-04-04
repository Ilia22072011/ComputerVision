import paramiko
from time import sleep
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect('169.254.56.206', 22, 'robot', 'maker')
i = 0
while 1==1:  
    i = int(input()) 
    inn, out, err = ssh.exec_command(f'echo "{i}" > /tmp/motor_commands')
    if i == 999:
        ssh.close()
        break