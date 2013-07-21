'''
Created on 2013-7-21

@author: Luo Fei
'''

from __future__ import absolute_import
from celery_test.celery import celery


@celery.task
def add(x,y):
    return x+y