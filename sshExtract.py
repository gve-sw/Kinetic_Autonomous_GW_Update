# contains function for SSH

import paramiko

# SSH into head end router, removed commas and spaces and return output
def sshExt():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('X.X.X.X',port=22,username='USERNAME',password='PASSWORD')
    stdin,stdout,stderr = ssh.exec_command('show crypto ikev2 sa detail | i Remote id|FC00:C15C')
    output=stdout.read().replace('\r\n',',')
    output=output.replace(' ','')
    return output
