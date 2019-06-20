# Scheduler:调度程序
import threading
import requests
from config import ACCOUNT_PASSWORD, proxyHost, proxyPort, proxyUser, proxyPass
from accountStorage import RedisClient
from pyppeteerGetCookie import getCookie



class Scheduler(object):
    def __init__(self):
        """
        初始化cookie池
        """
        # 创建cookie客户端
        self.client = RedisClient()
        # 当前要获取的用户名索引
        self.now_cookie_index = 0


    def run(self):
        # 轮询登录获取所有账号的cookie
        self.login_set_cookie_all()



    def login_set_cookie_all(self):
        for el in ACCOUNT_PASSWORD:
            username = el[0]
            password = el[1]
            self.login_set_cookie_one(username,password)
        self.refresh_cookie()


    def login_set_cookie_one(self,username, password):
        """
        登录账号获取cookie
        :param username: 用户名
        :param password: 密码
        :return:
        """
        cookie = getCookie(username, password)  # 登录获取cookie
        self.client.setAvailableCookie(username, cookie)  # 设置cookie


    def get_one_cookie_info(self):
        """轮询从redis中获取cookie 的接口"""
        username = ACCOUNT_PASSWORD[self.now_cookie_index][0]  # 判断要获取哪一个用户名对应cookie
        cookie = self.client.getUserCookie(username)
        if self.now_cookie_index + 1 >= len(ACCOUNT_PASSWORD):
            self.now_cookie_index = 0    # 修改当前要获取cookie对应username的索引
        else:
            self.now_cookie_index += 1
        return {"username":username,"cookie":cookie}


    def refresh_cookie(self):
        """
        持续刷新cookie，保持cookie可用性
        :return:
        """
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        all_cookies_dic = self.client.get_all_cookies()
        for username in all_cookies_dic:
            print('+++++++==   cookie定时刷新   ==+++++++++')
            cookie = all_cookies_dic[username]
            headers = {
                'cookie':cookie,
                'user-Agent': ua
            }
            # 要访问的目标页面
            targetUrl = 'http://www.taobao.com'

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
                "user": proxyUser,
                "pass": proxyPass,
            }

            proxies = {
                "http": proxyMeta,
                "https": proxyMeta,
            }

            requests.get(targetUrl, headers=headers, proxies=proxies)
        if self.client.cookieTotal() < 1:  # 此处 TODO 根据实际情况判断
            for i in self.client.get_all_UnavailableCookie_username():
                username = i
                password = self.client.getUserPassword(i)
                getCookie(username,password)
                print('过期后，重新登录')
        threading.Timer(20, self.refresh_cookie).start()  # 20秒刷新一次cookie


    def delete_and_set_Cookie(self,username, cookie):
        """
        根据用户名删除cookie
        :param username: 要删除的用户名
        :return:删除成功状态，1删除成功，0删除失败
        """
        delete_status = self.client.deleteCookie(username)
        set_status = self.client.setUnavailableCookie(username,cookie)
        return delete_status,set_status


scheduler_ = Scheduler()

