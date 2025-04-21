import paramiko
from time import sleep
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect('169.254.26.95', 22, 'robot', 'maker')
i = 0
while 1==1:  
    i = int(input()) 
    if i == 999:
        ssh.exec_command(f'echo 0 > /tmp/motor_commands')
        ssh.close()
        break
    inn, out, err = ssh.exec_command(f'echo "{i}" > /tmp/motor_commands')