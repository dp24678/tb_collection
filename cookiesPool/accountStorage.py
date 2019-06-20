# _*_coding:utf-8 _*_
#@Time    :2019/5/23 14:45
#@Author  :Dapan
#@Email : 248312738@qq.com
# accountStorage:账户信息存储模块
import redis
import sys
import time
import os
from config import *  # 单独运行文件时 from config import *



class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        # self.name = data_type  # 数据类型作为hash数据的key名称
        self.hashKeyUserInfo = "cookiePool:userInfo"
        self.AvailableCookieKey = "cookiePool:cookie"
        self.UnavailableCookieKey = "cookiePool:unavailable_cookie"
        # self.listKeyCookie = "cookiePool:cookie"
        self.init_db()  # 初始化数据库
        # self.now_cookie_index = 0  # 当前要获取的cookie索引
        print('======客户端初始化成功======',os.path.basename(__file__))


    def init_db(self):
        """
        初始化数据库
        :return:
        """
        for el in ACCOUNT_PASSWORD:  # field ：字段
            field = el[0]  # 字段,用户名
            value = el[1]  # value，密码
            self.db.hset(self.hashKeyUserInfo, field, value)
        print('======账户密码信息插入redis成功======',os.path.basename(__file__))


    def getUserPassword(self, username):
        """
        根据键名获取键值  获取密码
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.hashKeyUserInfo, username)  # db.hget(name,attr)   name 键，attr value的属性


    def deleteCookie(self, username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.AvailableCookieKey, username)


    def setAvailableCookie(self,username, cookie):
        """
        根据账户名将获取到的cookie设置到数据库中
        :param username:用户名
        :return:
        """
        self.db.hset(self.AvailableCookieKey, username, cookie)


    def setUnavailableCookie(self,username, cookie):
        """
        设置失效cookie
        :param username:用户名
        :return:
        """
        self.db.hset(self.UnavailableCookieKey, username, cookie)


    def getUserCookie(self,username):
        """
        根据账户名从数据库中获取cookie
        :param username: 用户名
        :return: 用户名对应的cookie
        """
        return self.db.hget(self.AvailableCookieKey, username)


    def cookieTotal(self):
        """
        获取hagh 键值对数目
        :return: 数目
        """
        return self.db.hlen(self.AvailableCookieKey)


    def get_all_cookies(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.AvailableCookieKey)


    def get_all_UnavailableCookie_username(self):
        return self.db.hkeys(self.UnavailableCookieKey)

    # def lpush_cookie(self,username,cookie):
    #
    #     value_ = str({username:cookie})
    #     self.db.lpush(self.listKeyCookie,value_)







    # def usernames(self):
    #     """
    #     获取所有账户信息
    #     :return: 所有用户名
    #     """
    #     return self.db.hkeys(self.name)
    #
    # def all(self):
    #     """
    #     获取所有键值对
    #     :return: 用户名和密码或Cookies的映射表
    #     """
    #     return self.db.hgetall(self.name)

    # def pollingGetCookie(self):
    #     """
    #     polling：轮询， 轮询获取cookie
    #     :return:
    #     """
    #     username = ACCOUNT_PASSWORD[self.now_cookie_index][0]
    #     cookie = self.getCookie(username)
    #
    #     if self.now_cookie_index + 1 == len(ACCOUNT_PASSWORD):
    #         self.now_cookie_index = 0    # 修改当前要获取的cookie索引 +1
    #     else:
    #         self.now_cookie_index += 1
    #
    #     return cookie


if __name__ == '__main__':
    client = RedisClient()
    # print(client.getUserPassword('铅笔头和作业本'))
    print(client.db.hkeys('cookiePool:cookie'))




