'''
Created on 2013-7-21

@author: wolf
'''

import time
def test():
    print time.time()
    print time.localtime(time.time())
    print time.strftime('%Y-%m-%d',time.localtime(time.time()))

if __name__ == '__main__':
    test()