'''
Created on 2013-7-21

@author: Luo Fei
'''

from celery import Celery
celery = Celery('tasks',broker='amqp://guest@localhost//')

@celery.task
def add(x,y):
    return x+y