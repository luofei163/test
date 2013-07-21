'''
Created on 2013-7-21

@author: Luo Fei
'''
from __future__ import absolute_import
from celery import Celery
celery = Celery('celery_test.celery',\
                broker='amqp://',
                backend='amqp://',
                include=['celery_test.tasks'])

celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
        )
if __name__ == '__main__':
    celery.start()
                