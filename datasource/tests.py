from django.test import TestCase

# Create your tests here.

import redis

# r = redis.Redis(host='127.0.0.1', port=6379,db=0)
# # r.set('name', 'zjc')   #添加
# print (r.get('name'))   #获取
#
def decorator_a(func):
    print('Get in decorator_a')
    def inner_a(*args, **kwargs):
        print ('Get in inner_a')
        ret =  func(*args, **kwargs)
        print('end in inner_a')
        return ret
    return inner_a

def decorator_b(func):
    print ('Get in decorator_b')
    def inner_b(*args, **kwargs):
        print('Get in inner_b')
        ret = func(*args, **kwargs)
        print('end in inner_b')
        return ret
    return inner_b
#
@decorator_b
@decorator_a
def f(x):
    print ('Get in f')
    return x * 2

f(1)

# from functools import wraps
#
# def deco(func):
#     @wraps(func) #加在最内层函数正上方
#     def wrapper(*args,**kwargs):
#         return func(*args,**kwargs)
#     return wrapper
#
# @deco
# def index():
#     '''哈哈哈哈'''
#     print('from index')
#
# import uuid
# print(uuid.uuid1())