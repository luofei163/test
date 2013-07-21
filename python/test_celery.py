'''
Created on 2013-7-21

@author: Luo Fei
'''
from celery_test.tasks import add
result = add.delay(10,9)
