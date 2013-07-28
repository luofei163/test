'''
Created on 2013-7-27

@author: Luo Fei
'''
import os
def list_dirs(dir):
    """
        List all folder and file 
    """
    
    target = os.listdir(dir)
    for t in target:
        p = os.path.join(dir,t)
        if os.path.isdir(p):
            list_dirs(p)
        else:
            print '%s is fiile under folder %s' % (t,dir)
# for path,dirs ,files in os.walk('1'):
#     for dir in dirs:
#         cur_dir =  os.path.join(path,dir)
#         list_dirs(cur_dir)    
list_dirs('1')

