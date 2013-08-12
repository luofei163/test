'''
Created on Jul 29, 2013

@author: Luo Fei
'''
import os
import subprocess
import sys

gerrit_ip = '10.1.80.222'
branch = "release-v2.3"
user = 'fei.luo'

def run_command(cmd, errorMessage):
    '''Execute cmd'''
    sign = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print cmd
    while sign.poll() == None:
        out = sign.stdout.readline()
        print out
    sign.wait()
    if sign.returncode != 0:
        if errorMessage != None:
            print errorMessage
        if exit == True:
            sys.exit(1)
        return False
    else:
        return True
    
def get_commit_msg():
   
    local_hooks = ".git/hooks"
    gerrit_hooks = "%s:/hooks/commit-msg" % gerrit_ip
    print os.getcwd()
    hooks_dir = os.path.join(os.getcwd(), local_hooks)
    cmd = 'scp -p -P 29418 %s@%s %s' % (user, gerrit_hooks, hooks_dir)
    cmd1 = 'wget http://%s:8081/tools/hooks/commit-msg %s' % (gerrit_ip, hooks_dir)
    if run_command(cmd, None) or run_command(cmd1, None):
        return True
        

def commit():
    msg = raw_input('Please enter commit message:' + os.linesep)
    cmd = 'git commit -m "%s"' % msg
    cmd1 = 'git push origin HEAD:refs/for/%s' % branch
    if run_command(cmd, None) and  run_command(cmd1, None):
        print  'Commit sucessfull!'

   

if get_commit_msg():
    commit()



